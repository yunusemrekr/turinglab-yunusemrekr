import pytest
import os
from io import StringIO
from contextlib import redirect_stdout
from turinglab import SingleTapeTM, RunResult

def test_binary_increment_basics():
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    # Test 1
    res = tm.run("1011")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "1100"
    # Test 2
    res = tm.run("0")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "1"
    # Test 3
    res = tm.run("111")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "1000"
    # Test 4
    res = tm.run("")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "1"
    # Test 5
    res = tm.run("10")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "11"

def test_unary_increment_basics():
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")
    # Test 1
    res = tm.run("11")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "111"
    # Test 2
    res = tm.run("1111")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "11111"
    # Test 3
    res = tm.run("1")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "11"
    # Test 4
    res = tm.run("")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "1"
    # Test 5
    res = tm.run("11111")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "111111"

def test_even_a_basics():
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")
    # Test 1
    res = tm.run("aa")
    assert res.accepted is True
    assert res.reason == "accept"
    # Test 2
    res = tm.run("a")
    assert res.accepted is False
    assert res.reason == "no_transition"
    # Test 3
    res = tm.run("bbaabb")
    assert res.accepted is True
    # Test 4
    res = tm.run("b")
    assert res.accepted is True
    # Test 5
    res = tm.run("bab")
    assert res.accepted is False

def test_binary_palindrome_basics():
    tm = SingleTapeTM.from_yaml("machines/binary_palindrome.yaml")
    # Test 1
    assert tm.run("1001").accepted is True
    # Test 2
    assert tm.run("010").accepted is True
    # Test 3
    assert tm.run("110").accepted is False
    # Test 4
    assert tm.run("1").accepted is True
    # Test 5
    assert tm.run("0000").accepted is True

def test_timeout_reason():
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")
    # Çok düşük max_steps vererek timeout'a düşürmek
    res = tm.run("1111", max_steps=2)
    assert res.accepted is False
    assert res.reason == "timeout"

def test_no_transition_reason():
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")
    # 'a' girildiğinde q_odd durumunda B okuyunca geçiş yok
    res = tm.run("a")
    assert res.accepted is False
    assert res.reason == "no_transition"

def test_invalid_yaml_value_error():
    # Bozuk YAML dosyası oluşturalım
    broken_yaml_path = "machines/broken.yaml"
    with open(broken_yaml_path, "w", encoding="utf-8") as f:
        f.write("name: broken\nstates: [q0") # Hatalı format
        
    with pytest.raises(ValueError) as exc:
        SingleTapeTM.from_yaml(broken_yaml_path)
    
    assert "Hatalı" in str(exc.value) or "hata" in str(exc.value)
    os.remove(broken_yaml_path)

def test_verbose_output_format():
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")
    f = StringIO()
    with redirect_stdout(f):
        tm.run("1", verbose=True)
    out = f.getvalue()
    
    assert "Adım 0" in out
    assert "Durum: q0" in out
    assert "Şerit:" in out
    assert "[1]" in out
    assert "Hareket: R" in out
