from src.secStructure import *


def test_processData():
    # Test1: ignoring peak position
    data = ['example/example1.fa', 'example/example2.fa']
    struct_data = ['example/exampleStructuralData1.fa', 'example/exampleStructuralData2.fa']
    k = 3
    top = 10
    peak = None
    feature = None
    cmd = False
    no_sec_peak = 1  # True

    # Executing

    process = SecStructure(data, data, k, peak, top, feature, cmd, struct_data, no_sec_peak)

    alphabet1 = process.getStructProfil1().getAlphabet()
    alphabet2 = process.getStructProfil2().getAlphabet()

    kmer_counts1 = process.getStructProfil1().getProfile()
    kmer_counts2 = process.getStructProfil2().getProfile()

    results = SecStructure.processData(process)

    template1 = results[0][0]
    template2 = results[1][0]

    dotbracket_string1 = results[0][1]
    dotbracket_string2 = results[1][1]

    # Testing

    assert len(alphabet1) == 6
    for e in ["S", "H", "B", "I", "M", "E"]:
        assert e in alphabet1

    assert len(alphabet2) == 2
    assert "S" in alphabet2
    assert "E" in alphabet2

    assert kmer_counts1 == {'EE': 4, 'ES': 1, 'SS': 11, 'SH': 1, 'HH': 3, 'II': 4, 'IS': 1, 'SM': 1, 'MM': 1, 'BB': 4,
                            'BS': 1}
    assert kmer_counts2 == {'SS': 20, 'EE': 7, 'ES': 3, 'SE': 2}

    assert template1 == "EEESSSIIISSSBBBSSSHHHSSSSSSIIISSSMMMSSSHHHSSSEEE"
    assert dotbracket_string1 == "...(((...(((...(((...))))))...)))...(((...)))..."

    assert template2 == "EEESSSSSSEEE"
    assert dotbracket_string2 == "...((()))..."

    # Test2: with peak position
    no_sec_peak = 0  # True

    # Executing

    process2 = SecStructure(data, data, k, peak, top, feature, cmd, struct_data, no_sec_peak)

    alphabet1 = process2.getStructProfil1().getAlphabet()
    alphabet2 = process2.getStructProfil2().getAlphabet()

    kmer_counts1 = process2.getStructProfil1().getProfile()
    kmer_counts2 = process2.getStructProfil2().getProfile()

    results = SecStructure.processData(process2)

    template1 = results[0][0]
    template2 = results[1][0]

    dotbracket_string1 = results[0][1]
    dotbracket_string2 = results[1][1]

    # Testing

    assert len(alphabet1) == 10
    for e in ["s", "h", "b", "i", "m", "E", "S", "B", "I", "E"]:
        assert e in alphabet1

    assert len(alphabet2) == 4
    for e in ["s", "S", "e", "E"]:
        assert e in alphabet2

    assert kmer_counts1 == {'eE': 1, 'Es': 1, 'sS': 1, 'Sh': 1, 'iI': 1, 'Is': 1, 'bB': 1, 'Bs': 1}
    assert kmer_counts2 == {'sS': 3, 'Ss': 2, 'sE': 1, 'Ee': 1, 'Se': 1}

    assert template1 == "EEESSSIIISSSBBBSSSSSSSSSIIISSSEEE"
    assert dotbracket_string1 == "...(((...(((...((())))))...)))..."

    assert template2 == "EEESSSSSSEEE"
    assert dotbracket_string2 == "...((()))..."


def test_createHeatMapColoring():
    pass


def test_createColorVector():
    pass


def test_helpAddIBloop():
    k = 3

    # Test 1: forward and all true
    template1 = ["EEE"]
    internalloop = True
    bulge = True
    forward = True

    # Execution
    new_template1 = helpAddIBloop(k, template1, internalloop, bulge, forward)

    # Test 2: backward and all true
    template2 = ["EEE", "SSS", "III", "SSS", "BBB", "SSS", "HHH"]
    internalloop = True
    bulge = True
    forward = False

    # Execution
    new_template2 = helpAddIBloop(k, template2, internalloop, bulge, forward)

    # Test 3: only internal loops, forward and backward
    template3_f = ["EEE"]
    template3_b = ["EEE", "SSS", "III", "SSS", "HHH"]
    internalloop = True
    bulge = False
    forward = True

    # Execution
    new_template3_f = helpAddIBloop(k, template3_f, internalloop, bulge, forward)

    forward = False
    new_template3_b = helpAddIBloop(k, template3_b, internalloop, bulge, forward)

    # Test 4: only bulges, forward and backward
    template4_f = ["EEE"]
    template4_b = ["EEE", "SSS", "BBB", "SSS", "HHH"]
    internalloop = False
    bulge = True
    forward = True

    # Execution
    new_template4_f = helpAddIBloop(k, template4_f, internalloop, bulge, forward)

    forward = False
    new_template4_b = helpAddIBloop(k, template4_b, internalloop, bulge, forward)

    # Testing
    assert new_template1 == ["EEE", "SSS", "III", "SSS", "BBB"]
    assert new_template2 == ["EEE", "SSS", "III", "SSS", "BBB", "SSS", "HHH", "SSS", "SSS", "III"]
    assert new_template3_f == ["EEE", "SSS", "III"]
    assert new_template3_b == ["EEE", "SSS", "III", "SSS", "HHH", "SSS", "III"]
    assert new_template4_f == ["EEE", "SSS", "BBB"]
    assert new_template4_b == ["EEE", "SSS", "BBB", "SSS", "HHH", "SSS"]


def test_element2dotbracket():
    k3 = 3
    k2 = 2
    k4 = 4

    # Test1 without multiloop
    elem_list1 = ["EEE", "SSS", "III", "SSS", "BBB", "SSS", "HHH", "SSS", "SSS", "III", "SSS", "EEE"]
    dotbracket_string1 = "...(((...(((...(((...))))))...)))..."

    # Test2 with multiloop
    elem_list2 = ["EE", "SS", "II", "SS", "HH", "SS", "II", "SS", "MM", "SS", "BB", "SS", "HH", "SS", "SS", "EE"]
    dotbracket_string2 = "..((..((..))..))..((..((..)))).."

    # Test 3 without loops
    elem_list3 = ["EEEE", "SSSS", "SSSS", "EEEE"]
    dotbracket_string3 = "....(((())))...."

    # Test 5 with everything
    elem_list4 = ["EEE", "SSS", "III", "SSS", "BBB", "SSS", "HHH", "SSS", "SSS", "III", "SSS", "MMM", "SSS", "HHH",
                  "SSS", "EEE"]
    dotbracket_string4 = "...(((...(((...(((...))))))...)))...(((...)))..."

    # Execution
    db1 = []
    db1.extend(element2dotbracket(elem_list1, k3, 0, 6, True))
    db1.extend(element2dotbracket(elem_list1, k3, 7, len(elem_list1) - 1, False))
    db1 = ''.join(db1)

    db2 = []
    db2.extend(element2dotbracket(elem_list2, k2, 0, 4, True))
    db2.extend(element2dotbracket(elem_list2, k2, 5, 8, False))
    db2.extend(element2dotbracket(elem_list2, k2, 9, 12, True))
    db2.extend(element2dotbracket(elem_list2, k2, 13, len(elem_list2) - 1, False))
    db2 = ''.join(db2)

    db3 = []
    db3.extend(element2dotbracket(elem_list3, k4, 0, 1, True))
    db3.extend(element2dotbracket(elem_list3, k4, 2, len(elem_list3) - 1, False))
    db3 = ''.join(db3)

    db4 = []
    db4.extend(element2dotbracket(elem_list4, k3, 0, 6, True))
    db4.extend(element2dotbracket(elem_list4, k3, 7, 11, False))
    db4.extend(element2dotbracket(elem_list4, k3, 12, 13, True))
    db4.extend(element2dotbracket(elem_list4, k3, 14, len(elem_list4) - 1, False))
    db4 = ''.join(db4)

    # testing
    assert db1 == dotbracket_string1
    assert db2 == dotbracket_string2
    assert db3 == dotbracket_string3
    assert db4 == dotbracket_string4