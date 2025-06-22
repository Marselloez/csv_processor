import csv
import re
import argparse
from tabulate import tabulate
from typing import List, Dict, Any

def parse_arguments():
    parser = argparse.ArgumentParser(description="CSV file processor with filter and aggregation")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--where", help="Filter condition in format 'column>value', 'column=value', or 'column<value'")
    parser.add_argument("--aggregate", help="Aggregation in format 'column=avg|min|max'")
    parser.add_argument("--order-by", help="Order by column in format 'column=asc|desc'")
    return parser.parse_args()

def read_csv(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

def apply_filter(data: List[Dict[str, Any]], condition: str) -> List[Dict[str, Any]]:
    if not condition:
        return data

    pattern = r"(.*?)(>=|<=|=|<|>)(.*)"
    match = re.fullmatch(pattern, condition.strip())
    if not match:
        raise ValueError("Unsupported or invalid filter format")

    column, operator, value = match.groups()
    column = column.strip()
    value = value.strip()

    if column not in data[0]:
        raise KeyError(f"Column '{column}' not found")

    if operator == "=":
        return [row for row in data if row[column] == value]

    try:
        return [
            row for row in data
            if eval(f"float(row[column]) {operator} float(value)")
        ]
    except Exception as e:
        raise ValueError(f"Filter evaluation error: {e}")

def apply_aggregation(data: List[Dict[str, Any]], operation: str) -> List[List[Any]]:
    column, func = map(str.strip, operation.split("="))
    values = [float(row[column]) for row in data]
    if func == "avg":
        return [["avg", sum(values) / len(values)]]
    elif func == "min":
        return [["min", min(values)]]
    elif func == "max":
        return [["max", max(values)]]
    else:
        raise ValueError("Unsupported aggregation function")

def apply_order_by(data: List[Dict[str, Any]], order_by: str) -> List[Dict[str, Any]]:
    if not order_by:
        return data
    column, direction = map(str.strip, order_by.split("="))
    reverse = direction.lower() == "desc"
    try:
        return sorted(data, key=lambda x: float(x[column]), reverse=reverse)
    except ValueError:
        return sorted(data, key=lambda x: x[column], reverse=reverse)

def main():
    args = parse_arguments()
    try:
        data = read_csv(args.file)
        if args.where:
            data = apply_filter(data, args.where)
        if args.order_by:
            data = apply_order_by(data, args.order_by)
        if args.aggregate:
            result = apply_aggregation(data, args.aggregate)
        else:
            result = data
        if result and isinstance(result[0], dict):
            print(tabulate(result, headers="keys", tablefmt="grid"))
        else:
            print(tabulate(result, headers="firstrow", tablefmt="grid"))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
