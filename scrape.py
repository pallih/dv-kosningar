import scraperwiki
import requests
import lxml.html
import json

URL_FRAMBOD_YFIRLIT = "http://www.dv.is/kosningar2013/frambod/"


def get_candidates(url):
    response = requests.get(url)
    root = lxml.html.fromstring(response.text)
    districts = root.xpath('//div[@class="district"]')
    for district in districts:
        district_dict = {}
        district_dict['district'] = district[0].text_content()
        parties = district.xpath('h3')
        for party in parties:
            district_dict['party'] = party.text_content()
            candidates = party.xpath('following-sibling::ul[@class="cand-list"]')
            for candidate in candidates:
                for x in candidate:
                    district_dict['candidate_url'] = x[0].attrib['href']
                    district_dict['candidate_placement'] = x[0][0].text
                    district_dict['candidate_name'] = x[0][1].text
                    district_dict['candidate_answer_status'] = x.attrib['class']
                    district_dict['candidate_photo_url'] = ""
                    district_dict['done'] = 0
                    scraperwiki.sqlite.save(['candidate_name'], data=district_dict, table_name='candidates')


def get_candidate_photo_url(candidate_url):
    candidate_dict = {}
    response = requests.get('http://dv.is'+candidate_url)
    root = lxml.html.fromstring(response.text)
    candidate_photo = root.xpath('//div[@class="cand-photo col2 right"]/img')
    #candidate_dict['candidate_photo_url'] = candidate_photo[0].attrib['src']
    return candidate_photo[0].attrib['src']

def get_questions(candidate_url):
    print candidate_url
    candidate_dict = {}
    response = requests.get('http://dv.is'+candidate_url+'afstada')
    print response.text
    root = lxml.html.fromstring(response.text)
    responses = root.xpath('//tr[@class="compare-question"]')
    batch = []
    for id,response in enumerate(responses):
        questions = {}
        questions['question'] = response[0].text
        questions['id'] = id+1
        batch.append(questions)
    scraperwiki.sqlite.save(['question'], data=batch, table_name='questions')

def get_candidate_responses():
    candidates = scraperwiki.sqlite.select('* from candidates where done=0 AND candidate_answer_status LIKE "cand ok"')
    if len(candidates) > 0:
        print len(candidates)
        for candidate in candidates:
            response = requests.get('http://dv.is'+candidate['candidate_url']+'afstada')
            root = lxml.html.fromstring(response.text)
            responses = root.xpath('//tr[@class="compare-question"]')
            batch = []
            for id,response in enumerate(responses):
                question = {}
                question['q_id'] = id+1
                question['response'] = response[1].text
                question['note'] = response[2].text
                question['candidate_name'] = candidate['candidate_name']
                batch.append(question)
            update_statement= 'update candidates SET done=1 WHERE candidate_url ='+ '"' + candidate['candidate_url']+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
            scraperwiki.sqlite.save(['q_id','candidate_name'], data=batch, table_name='question_responses')
            print 'saved'
        return True
    else:
        return False

def print_question(number):
    responses = scraperwiki.sqlite.select('* from question_responses where q_id=%s' % number)
    options = []
    for response in responses:
        options.append(response['response'])
    options = set(options)
    print options


# Get all the candidates
get_candidates(URL_FRAMBOD_YFIRLIT)
#print 'Got candidates'

# Get each candidate photo

# candidates = scraperwiki.sqlite.select('* from candidates where done=0')
# for candidate in candidates:
#    candidate_photo_url = get_candidate_photo_url(candidate['candidate_url'])
#    update_statement= 'update candidates SET candidate_photo_url='+ '"' +candidate_photo_url+ '"' +' WHERE candidate_url ='+ '"' + candidate['candidate_url']+ '"'
#    scraperwiki.sqlite.execute(update_statement)
#    scraperwiki.sqlite.commit()
    #print update_statement


# Get questions

candidates = scraperwiki.sqlite.select('* from candidates where candidate_answer_status LIKE "cand ok" limit 1')
for candidate in candidates:
    get_questions(candidate['candidate_url'])
print 'Got questions'

# Get each candidate response
while True:
    get_candidate_responses()

print 'done'

# print question response

# for number in range(1,67):
#     print_question(number)

