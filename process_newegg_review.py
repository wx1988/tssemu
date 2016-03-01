import re

def get_reviews(content):
    reviews_reg = "(<table class=\"grpReviews(\s|\S)*?</table>)"
    m = re.search(reviews_reg, content)
    if not m:
        return []
    reviews_str = m.group(1)
    print reviews_str
    review_reg = "(<tr>(\s|\S)*?</tr>)"
    review_para_reg = "(<p>(\s|\S)*?</p>)"
    con_list = []
    for m in re.findall(review_reg, reviews_str):
        review_str = m[0]
        for md in re.findall(review_para_reg, review_str):
            tmp_str = md[0]
            if tmp_str.count("<em>Cons") > 0:
                con_list.append(tmp_str)
    #print con_list
    return con_list

def test_get_reviews():
    fpath = "neweggreview/9SIA0AJ3S75119.html"
    fpath = "neweggreview/9SIA4UB3RF0795.html"
    content = open(fpath).read()
    print get_reviews(content)

if __name__ == "__main__":
    test_get_reviews()