# coding=utf-8

from poco.utils.query_util import build_query as bq


class UIDefine(object):
    """
    query表达式相关可以参照poco的Selector类

    expr := (l)
    - ``op0`` can be one of the following ('>', '/', '-'), each operator stands for as follows::

        '>': offsprings, select all offsprings matched expr1 from all roots matched expr0.
        '/': children, select all children matched expr1 from all roots matched expr0.
        '-': siblings, select all siblings matched expr1 from all roots matched expr0.
        '^': parent, select the parent of 1st UI element matched expr0. expr1 is always None.
b
    """
    MAIN_START = ('/', (('>', (bq('beginPanel'), bq('btn_start'))), bq('Text')))  # beginPanel>btn_start/Text
    MENU_VIEW = bq('levelSelect')
    MENU_DRAG_DROP = ('/', (MENU_VIEW, bq('drag_and_drop')))  # levelSelect/drag_and_drop
    MENU_INPUT = ('/', (MENU_VIEW, bq('basic')))  # levelSelect/basic
    MENU_LISTVIEW = ('/', (MENU_VIEW, bq('list_view')))  # levelSelect/basic

    INPUT_VIEW = bq('playBasic')
    INPUT_FILED = ('>', (INPUT_VIEW, bq('pos_input')))  # playBasic>pos_input

    LIST_VIEW = bq('playListView')
    LIST_SCROLLVIEW = ('>', (LIST_VIEW, bq('Scroll View')))  # playBasic>pos_input
    LIST_ITEM12 = ('>', (LIST_VIEW, bq(name=None, nameMatches='Text.*', text='Item 12')))
    LIST_SELECT = ('>', (LIST_VIEW, bq('list_view_current_selected_item_name')))

    DRAG_VIEW = bq('playDragAndDrop')
    DRAG_STAR = ('>', (DRAG_VIEW, bq('star')))  # playDragAndDrop>star
    DRAG_SHELL = ('>', (DRAG_VIEW, bq('shell')))  # playDragAndDrop>shell
    DRAG_SCORE = ('>', (DRAG_VIEW, bq('scoreVal')))  # playDragAndDrop>scoreVal
