def pair_elements_medias(lst):
    start_elements = lst[1::3]
    end_elements = lst[2::3]
    pairs = list(zip(start_elements, end_elements))
    return pairs

def pair_elements_heating(lst):
    start_elements = lst[0::3]
    end_elements = lst[1::3]
    pairs = list(zip(start_elements, end_elements))
    return pairs

def pair_elements_cooling(lst):
    start_elements = lst[2::3]
    end_elements = lst[3::3]
    pairs = list(zip(start_elements, end_elements))
    return pairs