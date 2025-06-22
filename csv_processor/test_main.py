import pytest
import subprocess
from main import apply_filter, apply_aggregation, apply_order_by

data = [
    {"name": "A", "price": "100", "rating": "4.5"},
    {"name": "B", "price": "200", "rating": "4.7"},
    {"name": "C", "price": "300", "rating": "4.2"}
]

def test_run_script_filter(tmp_path):
    test_file = tmp_path / "products.csv"
    test_file.write_text("name,price,rating\nA,100,4.5\nB,200,4.7")
    result = subprocess.run(
        ["python", "main.py", "--file", str(test_file), "--where", "price>150"],
        capture_output=True,
        text=True
    )
    assert "B" in result.stdout

def test_script_with_aggregation(tmp_path):
    import subprocess
    test_file = tmp_path / "products.csv"
    test_file.write_text("name,price,rating\nA,100,4.5\nB,200,4.7")
    result = subprocess.run(
        ["python", "main.py", "--file", str(test_file), "--aggregate", "price=avg"],
        capture_output=True,
        text=True
    )
    assert "avg" in result.stdout

def test_script_main_error(tmp_path):
    import subprocess
    # создаём повреждённый CSV
    test_file = tmp_path / "broken.csv"
    test_file.write_text("name;price;rating\nA;100;4.5")  # некорректный разделитель
    result = subprocess.run(
        ["python", "main.py", "--file", str(test_file), "--where", "price>100"],
        capture_output=True,
        text=True
    )
    assert "Error" in result.stdout

def test_filter_greater():
    result = apply_filter(data, "price>150")
    assert len(result) == 2

def test_filter_less():
    result = apply_filter(data, "rating<4.6")
    assert len(result) == 2
    assert result[0]["name"] == "A"
    assert result[1]["name"] == "C"

def test_filter_equal():
    result = apply_filter(data, "name=B")
    assert result[0]["name"] == "B"

def test_filter_no_match():
    result = apply_filter(data, "price>1000")
    assert result == []

def test_filter_and_order_only():
    result = apply_order_by(
        apply_filter(data, "rating>4.3"),
        "price=desc"
    )
    assert result[0]["price"] == "200"
    assert result[1]["price"] == "100"

def test_filter_invalid_operator():
    with pytest.raises(ValueError):
        apply_filter(data, "price<>100")

def test_filter_column_not_exist():
    from main import apply_filter
    import pytest
    with pytest.raises(KeyError):
        apply_filter(data, "nonexistent>10")

def test_aggregation_avg():
    result = apply_aggregation(data, "price=avg")
    assert round(result[0][1], 2) == 200.0

def test_aggregation_min():
    result = apply_aggregation(data, "rating=min")
    assert result[0][1] == 4.2

def test_aggregation_max():
    result = apply_aggregation(data, "price=max")
    assert result[0][1] == 300.0

def test_aggregation_invalid_func():
    with pytest.raises(ValueError):
        apply_aggregation(data, "price=sum")

def test_aggregation_invalid_column():
    with pytest.raises(KeyError):
        apply_aggregation(data, "wrongcol=avg")

def test_order_by_asc():
    result = apply_order_by(data, "price=asc")
    assert result[0]["price"] == "100"
    assert result[-1]["price"] == "300"

def test_order_by_desc():
    result = apply_order_by(data, "rating=desc")
    assert result[0]["rating"] == "4.7"
    assert result[-1]["rating"] == "4.2"

def test_order_by_invalid_column():
    with pytest.raises(KeyError):
        apply_order_by(data, "nope=asc")

