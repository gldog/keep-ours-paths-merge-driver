import logging

logger = logging.getLogger()


def replace_nth(s, search_token, replacement_token, position):
    start_search_at = 0
    for i in range(position):
        index_of_search_token = s.find(search_token, start_search_at)
        if index_of_search_token == -1:
            return ''
        if i == position - 1:
            return s[0:index_of_search_token] + replacement_token + s[index_of_search_token + len(search_token):]
        start_search_at = index_of_search_token + 1

    return ''


def replace_token(s, search_token, replacement_token, compare_to_reference):
    n = 1
    while True:
        # replace_nth() returns an empty string in case there is no searchToken at n.
        str_replaced_at_n = replace_nth(s, search_token, replacement_token, n)
        if not str_replaced_at_n:
            break

        # if !str_replaced_at_n.isEmpty() & & compareToReferencePredicate.test(str_replaced_at_n)) {
        is_equal = compare_to_reference(str_replaced_at_n)
        if is_equal:
            s = str_replaced_at_n
            break
        n += 1

    return s
