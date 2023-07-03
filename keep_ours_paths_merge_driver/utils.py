import logging

logger = logging.getLogger()


def replace_nth(s, search_token, replace_token, position):
    index_of_search_token = 0
    start_search_at = 0
    for i in range(position):
        index_of_search_token = s.find(search_token, start_search_at)
        if index_of_search_token == -1:
            return ''
        if i == position - 1:
            return s[0:index_of_search_token] + replace_token + s[index_of_search_token + len(search_token):]
        start_search_at = index_of_search_token + 1

    return ''


def replace_token(s, search_token, replace_token, compare_to_reference):
    logger.debug(f"replace_token(); search_token: {search_token}; replace_token: {replace_token}")
    str_replaced_at_n = ''
    n = 1
    while True:
        # replace_nth() returns an empty string in case there is no searchToken at n.
        str_replaced_at_n = replace_nth(s, search_token, replace_token, n)
        if not str_replaced_at_n:
            break

        # if !str_replaced_at_n.isEmpty() & & compareToReferencePredicate.test(str_replaced_at_n)) {
        is_equal = compare_to_reference(str_replaced_at_n)
        logger.debug(f"  is_equal: {is_equal}")
        if is_equal:
            s = str_replaced_at_n
            break
        n += 1

    return s
