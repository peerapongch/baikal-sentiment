import pickle
import regex as re
import pandas as pd
import html
import emoji
from transformers import AutoTokenizer
from typing import Collection, Callable

# this mf will comprise of mini methods and one function to be called outside

SPACE_SPECIAL_TOKEN = "<_>"
_TK_UNK, _TK_REP, _TK_WREP, _TK_URL, _TK_END = "<unk> <rep> <wrep> <url> </s>".split()

# cleaning
def replace_nbspace(text: str):
    if type(text) != str:
        return text
    nbspace = '\xa0'
    cleaned_text = re.sub(fr'{nbspace}', ' ', text)
    return cleaned_text

def remove_soft_hyphen(text: str):
    if type(text) != str:
        return text
    soft_hyphen = '\u00ad' # discretionary hyphen 
    cleaned_text = re.sub(fr'{soft_hyphen}', '', text)
    return cleaned_text

def remove_zero_width_nbspace(text: str):
    if type(text) != str:
        return text
    zero_width_nbspace = '\ufeff'
    cleaned_text = re.sub(fr'{zero_width_nbspace}', '', text)
    return

def strip_text(text: str):
    if type(text) != str:
        return text
    return text.strip()

def remove_thwiki_section(text:str):
    if type(text) != str:
        return text
    search_obj = re.search(r'Section::::', text)
    cleaned_text = text
    if search_obj:
        cleaned_text = re.sub(r'^Section::::', '', text)
        cleaned_text = re.sub(r'Section::::', '', text)
        cleaned_text = re.sub(r'\.$', '', cleaned_text)

    return cleaned_text

def fix_html(text: str) -> str:
    """
        List of replacements from html strings in `test`. (code from `fastai`)
        :param str text: text to replace html string
        :return: text where html strings are replaced
        :rtype: str
        :Example:
            >>> fix_html("Anbsp;amp;nbsp;B @.@ ")
            A & B.
    """
    re1 = re.compile(r"  +")
    text = (
        text.replace("#39;", "'")
        .replace("amp;", "&")
        .replace("#146;", "'")
        .replace("nbsp;", " ")
        .replace("#36;", "$")
        .replace("\\n", "\n")
        .replace("quot;", "'")
        .replace("<br />", "\n")
        .replace('\\"', '"')
        .replace(" @.@ ", ".")
        .replace(" @-@ ", "-")
        .replace(" @,@ ", ",")
        .replace("\\", " \\ ")
    )
    return re1.sub(" ", html.unescape(text))

def rm_brackets(text: str) -> str:
    """
        Remove all empty brackets and artifacts within brackets from `text`.
        :param str text: text to remove useless brackets
        :return: text where all useless brackets are removed
        :rtype: str
        :Example:
            >>> rm_brackets("hey() whats[;] up{*&} man(hey)")
            hey whats up man(hey)
    """
    # remove empty brackets
    new_line = re.sub(r"\(\)", "", text)
    new_line = re.sub(r"\{\}", "", new_line)
    new_line = re.sub(r"\[\]", "", new_line)
    # brakets with only punctuations
    new_line = re.sub(r"\([^a-zA-Z0-9ก-๙]+\)", "", new_line)
    new_line = re.sub(r"\{[^a-zA-Z0-9ก-๙]+\}", "", new_line)
    new_line = re.sub(r"\[[^a-zA-Z0-9ก-๙]+\]", "", new_line)
    # artifiacts after (
    new_line = re.sub(r"(?<=\()[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line)
    new_line = re.sub(r"(?<=\{)[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line)
    new_line = re.sub(r"(?<=\[)[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line)
    # artifacts before )
    new_line = re.sub(r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\))", "", new_line)
    new_line = re.sub(r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\})", "", new_line)
    new_line = re.sub(r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\])", "", new_line)
    return new_line

def replace_newlines(text: str) -> str:
    """
        Replace newlines in `text` with spaces.
        :param str text: text to replace all newlines with spaces
        :return: text where all newlines are replaced with spaces
        :rtype: str
        :Example:
            >>> rm_useless_spaces("hey whats\n\nup")
            hey whats  up
    """

    return re.sub(r"[\n]", " ", text.strip())

def rm_useless_spaces(text: str) -> str:
    """
        Remove multiple spaces in `text`. (code from `fastai`)
        :param str text: text to replace useless spaces
        :return: text where all spaces are reduced to one
        :rtype: str
        :Example:
            >>> rm_useless_spaces("oh         no")
            oh no
    """
    return re.sub(" {2,}", " ", text)

def replace_spaces(text: str, space_token: str = SPACE_SPECIAL_TOKEN) -> str:
    """
        Replace spaces with _
        :param str text: text to replace spaces
        :return: text where all spaces replaced with _
        :rtype: str
        :Example:
            >>> replace_spaces("oh no")
            oh_no
    """
    return re.sub(" ", space_token, text)

def replace_rep_after(text: str) -> str:
    """
    Replace repetitions at the character level in `text`
    :param str text: input text to replace character repetition
    :return: text with repetitive tokens removed.
    :rtype: str
    :Example:
        >>> text = "กาาาาาาา"
        >>> replace_rep_after(text)
        'กา'
    """

    def _replace_rep(m):
        c, cc = m.groups()
        return f"{c}"

    re_rep = re.compile(r"(\S)(\1{3,})")
    return re_rep.sub(_replace_rep, text)

#create tokenizer
def tokenize(
    text_list, 
    pretrained_name='airesearch/wangchanberta-base-att-spm-uncased'
    ):
  # if using spm tokenizer from wangchanberta pretrained 
  # then the special characters are already encoded
  tokenizer = AutoTokenizer\
  .from_pretrained(
      pretrained_name,
      revision='main',
      model_max_length=416,
      )
  return [tokenizer.tokenize(x) for x in text_list]

# post-rules
def ungroup_emoji(toks: Collection[str]) -> Collection[str]:
    """
    Ungroup Zero Width Joiner (ZVJ) Emojis
    See https://emojipedia.org/emoji-zwj-sequence/
    :param Collection[str] toks: list of tokens
    :return: list of tokens where emojis are ungrouped
    :rtype: Collection[str]
    :Example:
        >>> toks = []
        >>> ungroup_emoji(toks)
        []
    """
    res = []
    for tok in toks:
        if emoji.emoji_count(tok) == len(tok):
            res.extend(list(tok))
        else:
            res.append(tok)
    return res

def replace_wrep_post(toks: Collection[str]) -> Collection[str]:
    """
    Replace reptitive words post tokenization;
    fastai `replace_wrep` does not work well with Thai.
    :param Collection[str] toks: list of tokens
    :return: list of tokens where repetitive words are removed.
    :rtype: Collection[str]
    :Example:
        >>> toks = ["กา", "น้ำ", "น้ำ", "น้ำ", "น้ำ"]
        >>> replace_wrep_post(toks)
        ['กา', 'น้ำ']
    """
    previous_word = None
    rep_count = 0
    res = []
    for current_word in toks + [_TK_END]:
        if current_word == previous_word:
            rep_count += 1
        elif (current_word != previous_word) & (rep_count > 0):
            res += [previous_word]
            rep_count = 0
        else:
            res.append(previous_word)
        previous_word = current_word
    return res[1:]

def run_preprocess(
  read_dir = './data/data_in.pickle', 
  write_dir = './data/data_out.pickle'
  ):

  data = pickle.load(
    open(read_dir, 'rb')
  )

  df = pd.DataFrame(
      [{
        '_id': str(x['_id']),
        'text': ''.join(x['full_text'].split('_')[1:]),
        'preprocess_sentiment': x['sentiment'],
        } for x in data]
  )
  df['clean_text'] = df['text']

  # cleaning
  clean_fn_list = [replace_nbspace, remove_soft_hyphen, strip_text]
  # remove_soft_hyphen, remove_zero_width_nbspace, strip_text
  for fn in clean_fn_list:
    print(fn)
    df['clean_text'] = [fn(x) for x in df['clean_text']]
    print(df.shape)

  # preprocess
  pre_fn_list = [fix_html, rm_brackets, replace_newlines, rm_useless_spaces, replace_spaces, replace_rep_after]
  for fn in pre_fn_list:
    print(fn)
    df['clean_text'] = [fn(x) for x in df['clean_text']]
    print(df.shape)

  # tokenize
  tok_clean = tokenize(df['clean_text'])

  # post rules 
  tok_clean = [ungroup_emoji(x) for x in tok_clean]
  tok_clean = [replace_wrep_post(x) for x in tok_clean]

  # join back
  df['final_clean_text'] = [''.join(x) for x in tok_clean]

  pickle.dump(
    open(write_dir, 'wb')
  )

  return True