import textProcessing

TEST_SENTENCE1 = "Hello!! How are you, Mr. Green? Welcome home..."
TEST_SENTENCE2 = "p.m, etc."
TEST_SENTENCE3 = "Text without abbreviations. Just to check added num12word 54."


def test_count_sentences1():
    assert textProcessing.count_sentences(TEST_SENTENCE1) == 3


def test_count_sentences2():
    assert textProcessing.count_sentences(TEST_SENTENCE2) == 0


def test_count_sentences3():
    assert textProcessing.count_sentences(TEST_SENTENCE3) == 2


def test_count_non_declarative1():
    assert textProcessing.count_non_declarative(TEST_SENTENCE1) == 2


def test_count_non_declarative2():
    assert textProcessing.count_non_declarative(TEST_SENTENCE2) == 0


def test_count_non_declarative3():
    assert textProcessing.count_non_declarative(TEST_SENTENCE3) == 0


def test_get_all_words1():
    assert textProcessing.get_all_words(TEST_SENTENCE1) == ["Hello", "How", "are", "you", "Mr",
                                                            "Green", "Welcome", "home"]


def test_get_all_words2():
    assert textProcessing.get_all_words(TEST_SENTENCE2) == ["p", "m", "etc"]


def test_get_all_words3():
    assert textProcessing.get_all_words(TEST_SENTENCE3) == ["Text", "without", "abbreviations",
                                                            "Just", "to", "check", "added", "num12word"]


def test_count_sentence_length1():
    assert textProcessing.count_sentence_length(TEST_SENTENCE1) == 32 / 3


def test_count_sentence_length2():
    assert textProcessing.count_sentence_length(TEST_SENTENCE2) == 0


def test_count_sentence_length3():
    assert textProcessing.count_sentence_length(TEST_SENTENCE3) == 49 / 2


def test_count_word_length1():
    assert textProcessing.count_word_length("hello how are you?") == 14 / 4


def test_count_word_length2():
    assert textProcessing.count_word_length("he1lo how are you 123?") == 14 / 4


def test_count_word_length3():
    assert textProcessing.count_word_length("123 543.") == 0


def test_ngrams1():
    assert textProcessing.get_top_k_ngrams("ab bc ab bc ab bc kk", 2, 2) == [('ab bc', 3), ('bc ab', 2)]


def test_ngrams2():
    assert textProcessing.get_top_k_ngrams("ab bc ab bc ab kk 11 ab kk 11", 2, 3) == [('ab bc ab', 2), ('bc ab bc', 1)]

