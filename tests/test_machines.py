from turinglab import SingleTapeTM

def test_tm1_unary_to_binary():
    tm = SingleTapeTM.from_yaml("machines/unary_to_binary.yaml")
    # Test 1: 3 -> 11 (Kabul)
    res = tm.run("111")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "11"
    
    # Test 2: 4 -> 100 (Kabul)
    assert tm.run("1111").accepted is True
    
    # Test 3: 1 -> 1 (Kenar durum - tek karakter)
    assert tm.run("1").accepted is True
    
    # Test 4: Yanlış alfabe karakteri (Red)
    assert tm.run("110").accepted is False
    
    # Test 5: Baştan hatalı/bozuk format (Red)
    assert tm.run("B11").accepted is False

def test_tm2_binary_compare():
    tm = SingleTapeTM.from_yaml("machines/binary_compare.yaml")
    # Test 1: A > B aynı uzunluk (Kabul)
    assert tm.run("1100#1011").accepted is True
    
    # Test 2: A > B farklı uzunluk (Kabul)
    assert tm.run("100#11").accepted is True
    
    # Test 3: B > A (Red)
    assert tm.run("1011#1100").accepted is False
    
    # Test 4: A == B (Red)
    assert tm.run("1010#1010").accepted is False
    
    # Test 5: Kenar durum - kısa (Red)
    assert tm.run("0#10").accepted is False

def test_tm3_string_copy():
    tm = SingleTapeTM.from_yaml("machines/string_copy.yaml")
    # Test 1: Normal kopyalama (Kabul)
    assert tm.run("abba").accepted is True
    
    # Test 2: Tek karakter (Kenar durum - Kabul)
    assert tm.run("a").accepted is True
    
    # Test 3: Boş girdi (Kenar durum - Kabul)
    assert tm.run("").accepted is True
    
    # Test 4: Yanlış formatta içinde # olan (Red)
    assert tm.run("ab#ba").accepted is False
    
    # Test 5: Yanlış alfabe (Red)
    assert tm.run("abc").accepted is False

def test_tm4_divisible_by_4():
    tm = SingleTapeTM.from_yaml("machines/student_choice.yaml")
    # Test 1: 4 (100) (Kabul)
    assert tm.run("100").accepted is True
    
    # Test 2: 12 (1100) (Kabul)
    assert tm.run("1100").accepted is True
    
    # Test 3: 0 (0) (Kenar durum - Kabul)
    assert tm.run("0").accepted is True
    
    # Test 4: 2 (10) (Red)
    assert tm.run("10").accepted is False
    
    # Test 5: 7 (111) (Red)
    assert tm.run("111").accepted is False
