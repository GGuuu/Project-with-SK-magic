# -*- mode: python ; coding: utf-8 -*-

from hanspell import spell_checker
import pandas as pd
from konlpy.tag import Okt
from pprint import pprint
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import ListProperty
from kivy.core.window import Window

# 창의 크기를 설정합니다.
Window.size = (450, 600)

# 파일이 있는 경로를 담을 리스트입니다.
total_files = []
# 파일 리스트 안에서 선택한 파일의 인덱스를 나타냅니다.
selected_index = None


# 전체적인 데이터 전처리 작업을 수행합니다
def data_preprocessing(files_path):
    data = pd.DataFrame()

    for file in files_path:
        try:
            _data = pd.read_csv(file, engine='python', encoding='utf-8')
        except:
            _data = pd.read_csv(file, engine='python', encoding='cp949')

        data = pd.concat([data, _data], axis=0, ignore_index=True)

    # 평점 제거: G마켓은 모두 평점이 없기 때문
    data = data.drop(['rate'], axis=1)

    # 결측치 제거 (리뷰 없는 것)
    data = data.sort_values(['product_name'])
    data = data.reset_index(drop=True)
    data = data.dropna()

    # 반복 리뷰 삭제
    counts = data.groupby('review').size()
    remove_reviews = list(counts.index[counts > 10])

    mask = data['review'].isin(remove_reviews)
    data = data[~mask]
    data = data.reset_index(drop=True)

    # 길이 10이하 리뷰 제거
    mask = [len(i) > 10 for i in data['review']]
    data = data[mask]
    data = data.reset_index(drop=True)

    # ID & 리뷰 중복 제거
    data.drop_duplicates(["user", "review"], keep=False)

    return data


# 맞춤법 검사를 실시하는 함수입니다.
def spell(file):
    data = file
    for i in range(len(data)):
        try:
            review = data['review'][i]
            if len(review) <= 500:
                checked = spell_checker.check(review)
                data['review'][i] = checked.checked
            else:
                iteration = len(review)//500 + 1
                checked = ''
                for j in range(iteration):
                    _checked = spell_checker.check(review[j*500:(j+1)*500])
                    checked += _checked.checked
                data['review'][i] = checked
        except:
            pass

    return data


# 불용어를 제거합니다.
def remove_stopwords(file):
    data = file

    # korean_stopwords.csv에 있는 외부에서 가져온 한국어 불용어를 나열한 것입니다.
    stopwords = ['아', '휴', '아이구', '아이쿠', '아이고', '어', '나', '우리', '저희', '따라', '의해', '을', '를', '에', '의', '가', '으로', '로', '에게', '뿐이다', '의거하여', '근거하여', '입각하여', '기준으로', '예하면', '예를 들면', '예를 들자면', '저', '소인', '소생', '저희', '지말고', '하지마', '하지마라', '다른', '물론', '또한', '그리고', '비길수 없다', '해서는 안된다', '뿐만 아니라', '만이 아니다', '만은 아니다', '막론하고', '관계없이', '그치지 않다', '그러나', '그런데', '하지만', '든간에', '논하지 않다', '따지지 않다', '설사', '비록', '더라도', '아니면', '만 못하다', '하는 편이 낫다', '불문하고', '향하여', '향해서', '향하다', '쪽으로', '틈타', '이용하여', '타다', '오르다', '제외하고', '이 외에', '이 밖에', '하여야', '비로소', '한다면 몰라도', '외에도', '이곳', '여기', '부터', '기점으로', '따라서', '할 생각이다', '하려고하다', '이리하여', '그리하여', '그렇게 함으로써', '하지만', '일때', '할때', '앞에서', '중에서', '보는데서', '으로써', '로써', '까지', '해야한다', '일것이다', '반드시', '할줄알다', '할수있다', '할수있어', '임에 틀림없다', '한다면', '등', '등등', '제', '겨우', '단지', '다만', '할뿐', '딩동', '댕그', '대해서', '대하여', '대하면', '훨씬', '얼마나', '얼마만큼', '얼마큼', '남짓', '여', '얼마간', '약간', '다소', '좀', '조금', '다수', '몇', '얼마', '지만', '하물며', '또한', '그러나', '그렇지만', '하지만', '이외에도', '대해 말하자면', '뿐이다', '다음에', '반대로', '반대로 말하자면', '이와 반대로', '바꾸어서 말하면', '바꾸어서 한다면', '만약', '그렇지않으면', '까악', '툭', '딱', '삐걱거리다', '보드득', '비걱거리다', '꽈당', '응당', '해야한다', '에 가서', '각', '각각', '여러분', '각종', '각자', '제각기', '하도록하다', '와', '과', '그러므로', '그래서', '고로', '한 까닭에', '하기 때문에', '거니와', '이지만', '대하여', '관하여', '관한', '과연', '실로', '아니나다를가', '생각한대로', '진짜로', '한적이있다', '하곤하였다', '하', '하하', '허허', '아하', '거바', '와', '오', '왜', '어째서', '무엇때문에', '어찌', '하겠는가', '무슨', '어디', '어느곳', '더군다나', '하물며', '더욱이는', '어느때', '언제', '야', '이봐', '어이', '여보시오', '흐흐', '흥', '휴', '헉헉', '헐떡헐떡', '영차', '여차', '어기여차', '끙끙', '아야', '앗', '아야', '콸콸', '졸졸', '좍좍', '뚝뚝', '주룩주룩', '솨', '우르르', '그래도', '또', '그리고', '바꾸어말하면', '바꾸어말하자면', '혹은', '혹시', '답다', '및', '그에 따르는', '때가 되어', '즉', '지든지', '설령', '가령', '하더라도', '할지라도', '일지라도', '지든지', '몇', '거의', '하마터면', '인젠', '이젠', '된바에야', '된이상', '만큼', '어찌_든', '그위에', '게다가', '점에서 보아', '비추어 보아', '고려하면', '하게될것이다', '일것이다', '비교적', '좀', '보다더', '비하면', '시키다', '하게하다', '할만하다', '의해서', '연이서', '이어서', '잇따라', '뒤따라', '뒤이어', '결국', '의지하여', '기대여', '통하여', '자마자', '더욱더', '불구하고', '얼마든지', '마음대로', '주저하지 않고', '곧', '즉시', '바로', '당장', '하자마자', '밖에 안된다', '하면된다', '그래', '그렇지', '요컨대', '다시 말하자면', '바꿔 말하면', '즉', '구체적으로', '말하자면', '시작하여', '시초에', '이상', '허', '헉', '허걱', '바와같이', '해도좋다', '해도된다', '게다가', '더구나', '하물며', '와르르', '팍', '퍽', '펄렁', '동안', '이래', '하고있었다', '이었다', '에서', '로부터', '까지', '예하면', '했어요', '해요', '함께', '같이', '더불어', '마저', '마저도', '양자', '모두', '습니다', '가까스로', '하려고하다', '즈음하여', '다른', '다른 방면으로', '해봐요', '습니까', '했어요', '말할것도 없고', '무릎쓰고', '개의치않고', '하는것만 못하다', '하는것이 낫다', '매', '매번', '들', '모', '어느것', '어느', '로써', '갖고말하자면', '어디', '어느쪽', '어느것', '어느해', '어느 년도', '라 해도', '언젠가', '어떤것', '어느것', '저기', '저쪽', '저것', '그때', '그럼', '그러면', '요만한걸', '그래', '그때', '저것만큼', '그저', '이르기까지', '할 줄 안다', '할 힘이 있다', '너', '너희', '당신', '어찌', '설마', '차라리', '할지언정', '할지라도', '할망정', '할지언정', '구토하다', '게우다', '토하다', '메쓰겁다', '옆사람', '퉤', '쳇', '의거하여', '근거하여', '의해', '따라', '힘입어', '그', '다음', '버금', '두번째로', '기타', '첫번째로', '나머지는', '그중에서', '견지에서', '형식으로 쓰여', '입장에서', '위해서', '단지', '의해되다', '하도록시키다', '뿐만아니라', '반대로', '전후', '전자', '앞의것', '잠시', '잠깐', '하면서', '그렇지만', '다음에', '그러한즉', '그런즉', '남들', '아무거나', '어찌하든지', '같다', '비슷하다', '예컨대', '이럴정도로', '어떻게', '만약', '만일', '위에서 서술한바와같이', '인 듯하다', '하지 않는다면', '만약에', '무엇', '무슨', '어느', '어떤', '아래윗', '조차', '한데', '그럼에도 불구하고', '여전히', '심지어', '까지도', '조차도', '하지 않도록', '않기 위하여', '때', '시각', '무렵', '시간', '동안', '어때', '어떠한', '하여금', '네', '예', '우선', '누구', '누가 알겠는가', '아무도', '줄은모른다', '줄은 몰랏다', '하는 김에', '겸사겸사', '하는바', '그런 까닭에', '한 이유는', '그러니', '그러니까', '때문에', '그', '너희', '그들', '너희들', '타인', '것', '것들', '너', '위하여', '공동으로', '동시에', '하기 위하여', '어찌하여', '무엇때문에', '붕붕', '윙윙', '나', '우리', '엉엉', '휘익', '윙윙', '오호', '아하', '어쨋든', '만 못하다', '하기보다는', '차라리', '하는 편이 낫다', '흐흐', '놀라다', '상대적으로 말하자면', '마치', '아니라면', '쉿', '그렇지 않으면', '그렇지 않다면', '안 그러면', '아니었다면', '하든지', '아니면', '이라면', '좋아', '알았어', '하는것도', '그만이다', '어쩔수 없다', '하나', '일', '일반적으로', '일단', '한켠으로는', '오자마자', '이렇게되면', '이와같다면', '전부', '한마디', '한항목', '근거로', '하기에', '아울러', '하지 않도록', '않기 위해서', '이르기까지', '이 되다', '로 인하여', '까닭으로', '이유만으로', '이로 인하여', '그래서', '이 때문에', '그러므로', '그런 까닭에', '알 수 있다', '결론을 낼 수 있다', '으로 인하여', '있다', '어떤것', '관계가 있다', '관련이 있다', '연관되다', '어떤것들', '에 대해', '이리하여', '그리하여', '여부', '하기보다는', '하느니', '하면 할수록', '운운', '이러이러하다', '하구나', '하도다', '다시말하면', '다음으로', '에 있다', '에 달려 있다', '우리', '우리들', '오히려', '하기는한데', '어떻게', '어떻해', '어찌_어', '어때', '어째서', '본대로', '자', '이', '이쪽', '여기', '이것', '이번', '이렇게말하자면', '이런', '이러한', '이와 같은', '요만큼', '요만한 것', '얼마 안 되는 것', '이만큼', '이 정도의', '이렇게 많은 것', '이와 같다', '이때', '이렇구나', '것과 같이', '끼익', '삐걱', '따위', '와 같은 사람들', '부류의 사람들', '왜냐하면', '중의하나', '오직', '오로지', '에 한하다', '하기만 하면', '도착하다', '까지 미치다', '도달하다', '정도에 이르다', '할 지경이다', '결과에 이르다', '관해서는', '여러분', '하고 있다', '한 후', '혼자', '자기', '자기집', '자신', '우에 종합한것과같이', '총적으로 보면', '총적으로 말하면', '총적으로', '대로 하다', '으로서', '참', '그만이다', '할 따름이다', '쿵', '탕탕', '쾅쾅', '둥둥', '봐', '봐라', '아이야', '아니', '와아', '응', '아이', '참나', '년', '월', '일', '령', '영', '일', '이', '삼', '사', '오', '육', '륙', '칠', '팔', '구', '이천육', '이천칠', '이천팔', '이천구', '하나', '둘', '셋', '넷', '다섯', '여섯', '일곱', '여덟', '아홉', '령', '영']

    stopwords = [i.split(' ') for i in stopwords]
    stopwords = [j for i in stopwords for j in i]

    # 가지고 있는 데이터에서 추가적으로 제거하고 싶은 불용어를 custom_stopwords에 넣습니다.
    custom_stopwords = ['합니다', '있어서', '있는', '거', '듯', '더',
                        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ',
                        'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', '개',
                        '긋', '껄', '룽', '되', '하', '들', '나', '디', '여리', 'ㅣ', '어귀', '차']
    stopwords += custom_stopwords

    for i in range(len(data)):
        review = data['review'][i]
        review = review.split(' ')
        new_token = [i for i in review if i not in stopwords]

        data['review'][i] = ' '.join(new_token)

    return data


# 단어를 토큰화합니다.
def tokenizer_okt(file):
    okt = Okt()

    def keywords(pos, tags=['Noun', 'Verb', 'Adjective']):
        words = []
        for p in pos:
            if p[1] in tags:
                words.append(p[0])
        return words

    df = file
    token = []
    for i in df.review.index:
        try:
            token.append(keywords(pos=okt.pos(df.review[i], norm=True, stem=True)))
        except:
            token.append([])

    return token


# LDA를 실행합니다.
def lda_visualization(file, num_Topics):
    sentences = file['review']

    # 1. Okt를 이용해 어휘화합니다.
    mecab = Okt()
    sentences_tag = []
    for sentence in sentences:
        morph = mecab.pos(sentence)
        sentences_tag.append(morph)
    selected_mec = []
    n_sentence = 0

    nouns_tag = []
    for sentence in sentences:
        morph = mecab.nouns(sentence)
        nouns_tag.append(morph)

    for sentence1 in sentences_tag:
        selected_mec.append([])
        for word, tag in sentence1:
            if tag in ['NNG', 'VV']:
                selected_mec[n_sentence].append(word)
        n_sentence += 1

    while [] in selected_mec:
        selected_mec.remove([])

    token = tokenizer_okt(file)
    selected_mec += token

    # 2. 사전을 만듭니다.
    id2word = gensim.corpora.Dictionary(selected_mec)

    # 3. 코퍼스를 생성합니다.
    texts = selected_mec

    # 4. 문서 빈도를 확인합니다.
    corpus = [id2word.doc2bow(text) for text in texts]

    # 5. 사람이 읽을 수 있는 형식의 코퍼스를 생성합니다.
    [[(id2word[id], freq) for id, freq in cp] for cp in corpus[:3]]

    num_topics = num_Topics
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics,
                                                random_state=100, update_every=1, chunksize=100,
                                                passes=10, alpha='auto', per_word_topics=True)

    # 6. 키워드를 출력합니다.
    pprint(lda_model.print_topics())

    # 7. 복잡도를 계산합니다.
    print('Perplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

    # 8. 일관성 점수를 계산합니다.
    coherence_model_lda = CoherenceModel(model=lda_model, texts=selected_mec, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)

    # 9. 토픽을 시각화합니다.
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    file_name = 'LDA_' + str(num_Topics) + ' topics.html'
    pyLDAvis.save_html(vis, file_name)
    return vis


# 파일을 선택하는 화면을 만들기 위한 클래스입니다.
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    bcolor = ListProperty([.4, .5, .5])

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            global selected_index
            selected_index = index

# 스크롤을 내리며 볼 수 있도록 하는 RecycleView 클래스입니다.
class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in total_files]

    # 파일을 추가하거나 제거할 때마다 업데이트해주는 함수입니다.
    def files_label(self):
        self.data.clear()
        self.data = [{'text': str(x)}for x in total_files]
        self.refresh_from_data()


# csv 파일이 아닌 경우 뜨는 팝업창입니다.
class FileError(Popup):
    pass


# 이미 존재하는 파일을 추가할 경우 뜨는 팝업창입니다.
class Exist_file(Popup):
    pass


# 파일을 선택하는 스크린을 담은 클래스입니다.
class Filechooser(Screen):
    files = []

    # 파일을 선택하면 밑에 선택한 파일의 이름을 볼 수 있도록 해줍니다.
    def select(self, *args):
        try:
            self.label.text = args[1][0]
        except:
            pass

    # Add 버튼을 누르면 파일이 추가되도록 하는 함수입니다.
    def add(self, *args):
        if ('.csv' in self.label.text or '.CSV' in self.label.text) and self.label.text not in total_files:
            self.files.append(self.label.text)
            total_files.append(self.label.text)
        elif self.label.text in total_files:
            pop = Exist_file()
            pop.open()
        else:
            pop = FileError()
            pop.open()

    # Back 버튼을 누르면 다시 원래 화면으로 돌아가는 함수입니다.
    def back(self, *args):
        self.parent.current = 'main'
        self.parent.update()


# 파일이 존재하지 않는데 Implement LDA 버튼을 누르면 뜨는 팝업창입니다.
class NoFile(Popup):
    pass


# 크롤링한 데이터의 형식이 맞지 않을 때 뜨는 팝업창입니다.
class ColumnError(Popup):
    pass


# 전처리한 후, 남은 리뷰 데이터가 없을 때 뜨는 팝업창입니다.
class NoReview(Popup):
    pass


# LDA를 모두 마치고 난 후 뜨는 팝업창입니다.
class Finish(Popup):
    pass


# 메인 화면입니다.
class MyLayout(Screen):
    # 선택한 인덱스의 번호를 나타냅니다.
    index = None
    # 토픽의 개수를 나타냅니다.
    num = 5

    # Implement LDA 버튼을 눌렀을 때 실행되는 함수입니다.
    def do_process(self):
        try:
            self.num = int(self.ids.topic_input.text)
        except:
            pass
        if len(total_files) == 0:
            pop = NoFile()
            pop.open()
            return
        # 먼저 전체적인 전처리를 해줍니다.
        try:
            preprocessed_data = data_preprocessing(total_files)
            if len(preprocessed_data)==0:
                pop = NoReview()
                pop.open()
                return
        except:
            pop = ColumnError()
            pop.open()
            return
        # 맞춤법 검사를 합니다.
        checked_data = spell(preprocessed_data)
        # 그 다음, 불용어를 제거해줍니다.
        stopwords_data = remove_stopwords(checked_data)
        # 마지막으로 LDA를 실행합니다.
        lda_visualization(stopwords_data, self.num)
        # 모두 실행이 되고 난 후 파일 리스트 안의 파일들을 제거하고 업데이트합니다.
        total_files.clear()
        self.parent.update()
        # 이후 끝났다는 팝업창을 만듭니다.
        pop = Finish()
        pop.open()
        return

    # Delete 버튼을 누르면 선택된 파일을 제거합니다.
    def delete_selected(self):
        try:
            selection = selected_index
            total_files.pop(selection)
            self.parent.update()
        except:
            pass


# 스크린의 전환을 할 수 있게 해주는 클래스입니다.
class WindowManager(ScreenManager):
    def update(self):
        self.ids.main.ids.file_list.files_label()

# Kivy를 통해서 만든 프로그램으로, 아래의 내용으로 레이아웃을 설정합니다.
# 아래와 같이 길게 만들지 않고, kv 파일을 따로 만들어서 간결하게 코드를 유지할 수도 있습니다.
kv = Builder.load_string('''
WindowManager:
    MyLayout:
        id: main
    Filechooser:
        id: chooser

<SelectableLabel>:
    # 배경의 크기와 배경 색상을 설정합니다.
    bcolor: root.bcolor
    canvas.before:
        Color:
            rgb: (.6, .7, .6) if self.selected else self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
<RV>:
    # 파일 선택 화면에서 다중 선택이 가능하게 하는 등 여러가지 설정을 할 수 있습니다.
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False

<MyLayout>:
    padding: 10
    spacing: 10
    name: 'main'
    size: root.width, root.height
    GridLayout:
        cols:1
        canvas.before:
            Color:
                rgb: .4, .5, .5
            Rectangle:
                pos: self.pos
                size: self.size
        RV:
            id: file_list
            size_hint: None, None
            size: (root.width, root.height/10*7.35)
        BoxLayout:
            size_hint: None, None
            size: (root.width, root.height/15)
            Label:
                text: 'Topic Num: '
                font_size: 25
                pos: (0, root.height/10)
                canvas.before:
                    Color:
                        rgb: .5, .5, .4
                    Rectangle:
                        pos: self.pos
                        size: self.size
            TextInput:
                id: topic_input
                font_size: 25
                text: ""
        GridLayout:
            Button:
                id: button
                text: 'Select File'
                size_hint: None, None
                font_size: 25
                pos: 0, root.height/10-1
                size: (root.width/3*2, root.height/10)
                on_release: root.manager.current = 'file_chooser'
            Button:
                id: delete
                text: 'Delete'
                size_hint: None, None
                pos: root.width/3*2, root.height/10-1
                font_size: 25
                size: (root.width/3, root.height/10)
                on_release: root.delete_selected()
        Button:
            id: make
            text: 'Implement LDA'
            size_hint: None, None
            font_size: 30
            size: (root.width, root.height/10)
            canvas.before:
                Rectangle:
                    pos: self.pos
                    size: self.size
            on_release: root.do_process()

<FileError>:
    label: label

    title: 'File Error'
    content: label
    size_hint: (None, None)
    size: (400, 100)

    Label:
        id: label
        text: "Please select 'csv' file!"

<Exist_file>:
    label: label

    title: 'Exist File'
    content: label
    size_hint: (None, None)
    size: (400, 100)

    Label:
        id: label
        text: "This file is already added!"

<NoFile>:
    label: label

    title: 'No File'
    content: label
    size_hint: (None, None)
    size: (400, 100)

    Label:
        id: label
        text: "There is no files added in list!"


<ColumnError>:
    label: label

    title: 'Column Error'
    content: label
    size_hint: (None, None)
    size: (400, 100)

    Label:
        id: label
        text: "Column is not matched with ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source']"


<NoReview>:
    label: label

    title: 'No Review'
    content: label
    size_hint: (None, None)
    size: (400, 100)

    Label:
        id: label
        text: "There is no review left after preprocessing!"
        
<Finish>:
    label: label

    title: 'Process'
    content: label
    size_hint: (None, None)
    size: (400, 100)

    Label:
        id: label
        text: "LDA html file is downloaded successfully!"


<Filechooser>:
    name: 'file_chooser'
    label: label
    # main: main

    # Providing the orentation
    orientation: 'vertical'

    # Creating the File list / icon view
    BoxLayout:
        size_hint_y: 0.87
        pos: (0,root.height/6.8)
        # Creating list view one side
        FileChooserListView:
            canvas.before:
                Color:
                    rgb: .4, .5, .5
                Rectangle:
                    pos: (0,0)
                    size: self.size
            on_selection: root.select(*args)
            dirselect: True

    # Adding label
    Label:
        id: label
        size_hint_y: .05
        pos: (0, root.height/10)
        canvas.before:
            Color:
                rgb: .5, .5, .4
            Rectangle:
                pos: self.pos
                size: self.size

    BoxLayout:
        size_hint: None, None
        size: (root.width, root.height/10)
        cols: 2
        Button:
            id: button
            text: 'Add'
            font_size: 25
            size_hint_y: 1
            size_hint: None, None
            size: root.width*0.8, root.height*0.1
            pos: (0,root.height/20)
            canvas.before:
                Color:
                    rgb: .5, .5, .6
                Rectangle:
                    pos: self.pos
                    size: self.size
            on_press: root.add(*args)

        Button:
            id: to_main
            text: 'Back'
            font_size: 25
            size_hint_y: 1
            background_color: (1,0,0,1)
            canvas.before:
                Color:
                    rgb: .5, .5, .6
                Rectangle:
                    pos: self.pos
                    size: self.size
            on_press: root.back()
''')


# 지금까지 만든 앱을 실행할 수 있도록 하는 클래스입니다.
class MainApp(App):
    def build(self):
        return kv


# 메인 함수에는 앱이 실행되도록 객체를 만들고 run()을 통해 실행합니다.
if __name__ == '__main__':
    MainApp().run()