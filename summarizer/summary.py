from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import googletrans
from googletrans import Translator

translator = Translator()
text_str = '''
కోర్ బ్రాంచ్‌ల్లో కలిసొచ్చే సర్టిఫికేషన్స్...
టెక్నికల్ ఎడ్యుకేషన్ సర్టిఫికేషన్ కోర్సులంటే ఎక్కువ మంది ఐటీ, 
కంప్యూటర్ సైన్స్ కోర్సులకుసంబంధించినవేనని భావిస్తారు. ఐటీ/సాఫ్ట్‌వేర్ రంగాలకు 
పెరుగుతున్న ప్రాధాన్యం, అవసరాలే దీనికి కారణం. అయితే కోర్ బ్రాంచ్‌లుగా పేరొందిన
విభాగాల్లోనూ ఇప్పుడు జాబ్ ఓరియెంటెడ్ సర్టిఫికెట్ కోర్సులు అందుబాటులోకి వస్తున్నాయి.
ముఖ్యంగా సివిల్, మెకానికల్ బ్రాంచ్‌ల విద్యార్థులకు జాబ్ మార్కెట్లో అవకాశాలు
అందించేందుకు ఈ సర్టిఫికేషన్స్ దోహదపడుతున్నాయి. ఈ క్రమంలో సివిల్,
మెకానికల్ ఇంజనీరింగ్ విభాగాల్లో ప్రాచుర్యం పొందిన సర్టిఫికెట్ కోర్సుల వివరాలు.
సంప్రదాయ ఇంజనీరింగ్ బ్రాంచ్‌లుగా, క్షేత్రస్థాయి విధులకు అధిక ప్రాధాన్యం
ఉండే బ్రాంచ్‌లుగా సివిల్ ఇంజనీరింగ్, మెకానికల్ ఇంజనీరింగ్ గుర్తింపు సాధించాయి. కానీ 
టెక్నాలజీ ఆవిష్కరణలతో ఈ రంగాలు ఇప్పుడు ఆధునికతను సంతరించుకుంటున్నాయి. ఈ 
క్రమంలోనే కొత్త నైపుణ్యాల సముపార్జన అవసరమైంది. ఉదాహరణకు గతంలో ఒక నిర్మాణానికి
సంబంధించి డిజైన్ రూపొందించాలంటే.. సివిల్ ఇంజనీర్ సదరు ప్రదేశాన్ని ప్రత్యక్షంగా పరిశీలించి,
డ్రాయింగ్, డిజైన్ కార్యకలాపాలు నిర్వహించేవారు. కానీ ఇప్పుడు ట్రెండ్ మారింది.
కంప్యూటర్ ముందు కూర్చుని, నిర్దిష్ట ప్రమాణాల మేరకు ఆటోమేషన్ విధానంలో డిజైన్,
డ్రాయింగ్ రూపొందిస్తున్నారు. ఇదే విధంగా మెకానికల్ ఇంజనీరింగ్‌లోనూ ఉత్పత్తి రూపకల్పన,
పర్యవేక్షణకు సంబంధించి ఆధునిక పద్ధతులు అందుబాటులోకి వచ్చాయి. వీటికి సంబంధించి
ప్రత్యేక కోర్సులు కూడా ఆవిష్కృతమవుతున్నాయి.'''

tel = translator.translate(text_str, src = 'te')

def _create_frequency_table(text_str) -> dict:
    stopWords = set(stopwords.words("english")) #remove the stopwords like a, an, the, is, etc.
    words = word_tokenize(text_str) #tokenizes the string
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    return freqTable


def _score_sentences(sentences, freqTable) -> dict:
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = len(word_tokenize(sentence))
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]
        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence
    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]
    
    average = (sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''
    
    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
            summary += " " + sentence
            sentence_count += 1
    return summary


def run_summarization(text):
    freq_table = _create_frequency_table(text)
    sentences = sent_tokenize(text)
    sentence_scores = _score_sentences(sentences, freq_table)
    threshold = _find_average_score(sentence_scores)
    summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold)
    return summary

if __name__ == '__main__':
    result = run_summarization(tel.text)
    print(result)
    tel = translator.translate(result, src = 'en', dest = 'te')
    print(tel.text)
