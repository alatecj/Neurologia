def calc_faq(exa):
    total = 0
    for i in exa.exam_responses.all():
        total += i.choice.points
    return f"Výsledok vyšetrenia je {total} bodov."


def calc_hads(exa):
    response_dict = {}
    responses = exa.exam_responses.all()
    for response in responses:
        response_dict[response.question.sequence] = response.choice.points
    vseobecne = sum(response_dict.values())
    uzkost = response_dict.pop(2) + response_dict.pop(4) + response_dict.pop(6) + response_dict.pop(8) + \
        response_dict.pop(11) + response_dict.pop(12) + response_dict.pop(14)
    depresia = sum(response_dict.values())
    result = f"Všeobecné výsledky: {vseobecne} "
    if vseobecne <= 7:
        result += "(norma)"
    elif vseobecne >= 11:
        result += "(patológia)"
    else:
        result += "(hraničná hodnota)"
    result += f", úzkosť: {uzkost} "
    if uzkost >= 6:
        result += "(patológia)"
    result += f", depresia: {depresia} "
    if depresia >= 6:
        result += "(patológia)"
    return result


def calc_liverpool(exa):
    response_list = []
    responses = exa.exam_responses.all()
    for response in responses:
        tup = (response.question.eval_sequence, response.choice.points)
        response_list.append(tup)
    response_list = sorted(response_list)
    zavaznost, postiktalny = 0, 0
    for x in range(9):
        zavaznost += response_list.pop(0)[1]
    postiktalny = sum(i[1] for i in response_list)
    result = f"Závažnosť: {zavaznost} bodov, postiktálny stav: {postiktalny} bodov."
    return result


def calc_sf36(exa):
    responses = exa.exam_responses.all()
    response_dict = {}
    for response in responses:
        response_dict[response.question.sequence] = response.choice.points
    general_health = (response_dict.pop(1) + response_dict.pop(33) + response_dict.pop(34) + response_dict.pop(
        35) + response_dict.pop(36)) / 5
    pain = (response_dict.pop(21) + response_dict.pop(22)) / 2
    social_func = (response_dict.pop(20) + response_dict.pop(32)) / 2
    emotional_wb = (response_dict.pop(24) + response_dict.pop(25) + response_dict.pop(26) + response_dict.pop(
        28) + response_dict.pop(30)) / 5
    energy_fatigue = (response_dict.pop(23) + response_dict.pop(27) + response_dict.pop(29) + response_dict.pop(31)) / 4
    role_emotional = (response_dict.pop(17) + response_dict.pop(18) + response_dict.pop(19)) / 3
    role_physical = (response_dict.pop(13) + response_dict.pop(14) + response_dict.pop(15) + response_dict.pop(16)) / 4
    health_change = response_dict.pop(2)
    phys_func = sum(response_dict.values()) / len(response_dict)
    result = f"Fyzické obmedzenia: {phys_func:.0f},  " \
             f"obmedzenia v dôsledku fyzického zdravia: {role_physical:.0f}, " \
             f"obmedzenia v dôsledku emocionálnych problémov: {role_emotional:.0f}, " \
             f"energia/únava: {energy_fatigue:.0f}, " \
             f"telesná bolesť: {pain:.0f}, " \
             f"všeobecné zdravie: {general_health:.0f}, " \
             f"sociálne fungovanie: {social_func:.0f}, " \
             f"emocionálna pohoda: {emotional_wb:.0f}, " \
             f"zmena zdravotného stavu: {health_change:.0f}."
    return result
