from transitions.extensions import GraphMachine
from utils import send_text_message, send_text_button, send_hot, send_new, send_search, send_text_drama_button, send_drama, send_taiwan_hot_movie, send_usa_hot_movie, send_new_movie
from utils import send_back

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # 1 handle error
    def is_going_to_help(self, event):
        button = ["本月熱門", "最近新作", "搜尋動畫", "熱門討論", "相關新聞", 
                    "熱門電影", "熱門美劇", "搜尋電影美劇",
                    "台灣票房","美國票房","本周上映",
                    "熱門戲劇", "熱門綜藝","各國熱門戲劇"]
        text = event.message.text
        if text not in button:
            return True
        # return text.lower() == "go to state1"

    def on_enter_help(self, event):
        print("I'm entering help\n")
        reply_token = event.reply_token
        send_text_button(reply_token, "請輸入 ...")
        self.go_back()

    def on_exit_help(self):
        print("Leaving help")


    #2 搜尋動畫
    def is_going_to_search(self, event):
        text = event.message.text
        return text.lower() == "搜尋動畫"

    def on_enter_search(self, event):
        print("I'm entering search")
        
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入動漫名稱")
        # self.go_back()

    def on_exit_search(self, *args, **kwargs):
        print("Leaving search")


    # 2.1 search name -----------------------------------------   
    def is_going_to_name(self, event):
        text = event.message.text
        # return text.lower() == "go to search"
        return True

    def on_enter_name(self, event):
        print("I'm entering name")
        reply_token = event.reply_token
        text = event.message.text
        print(text +'\n')
        send_search(reply_token, text)
        send_back(reply_token)

    def on_exit_name(self, *args, **kwargs):
        print("Leaving name")


    #3 熱門討論
    def is_going_to_discussion(self, event):
        text = event.message.text
        return text.lower() == "eat"

    def on_enter_discussion(self, event):
        print("I'm entering discussion\n")
        reply_token = event.reply_token
        send_text_message(reply_token, "熱門討論...")
        self.go_back()

    def on_exit_discussion(self):
        print("Leaving discussion\n")


    #4 本月熱門
    def is_going_to_hot(self, event):
        text = event.message.text
        return text.lower() == "本月熱門"

    def on_enter_hot(self, event):
        print("I'm entering hot\n")
        reply_token = event.reply_token
        send_hot(reply_token)
        self.go_back()

    def on_exit_hot(self):
        print("Leaving hot\n")


    #5 最近新作
    def is_going_to_new(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "最近新作"
        else:
            return False

    def on_enter_new(self, event):
        print("I'm entering new\n")
        reply_token = event.reply_token
        send_new(reply_token)
        self.go_back()

    def on_exit_new(self):
        print("Leaving new\n")

    # ------------------------------------------------------------------
    # movie
    # taiwan movie
    def is_going_to_taiwan(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "台灣票房"
        else:
            return False

    def on_enter_taiwan(self, event):
        print("I'm entering tw\n")
        reply_token = event.reply_token
        send_taiwan_hot_movie(reply_token)
        self.go_back()

    def on_exit_taiwan(self):
        print("Leaving tw\n")


    # usa movie
    def is_going_to_usa(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "美國票房"
        else:
            return False

    def on_enter_usa(self, event):
        print("I'm entering usa\n")
        reply_token = event.reply_token
        send_usa_hot_movie(reply_token)
        self.go_back()

    def on_exit_usa(self):
        print("Leaving usa\n")

    # week movie
    def is_going_to_week(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "本周上映"
        else:
            return False

    def on_enter_week(self, event):
        print("I'm entering week\n")
        reply_token = event.reply_token
        send_new_movie(reply_token)
        self.go_back()

    def on_exit_week(self):
        print("Leaving week")

    # -----------------------------------------------------------------------
    # drama
    # hot drama
    def is_going_to_hot_drama(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "熱門戲劇"
        else:
            return False

    def on_enter_hot_drama(self, event):
        print("I'm entering 戲劇\n")
        reply_token = event.reply_token
        send_drama(reply_token, "hot")
        self.go_back()

    def on_exit_hot_drama(self):
        print("Leaving 戲劇")

     # hot taiwan
    def is_going_to_hot_taiwan(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "熱門綜藝"
        else:
            return False

    def on_enter_hot_taiwan(self, event):
        print("I'm entering 綜藝\n")
        reply_token = event.reply_token
        send_drama(reply_token, "entertain")
        self.go_back()

    def on_exit_hot_taiwan(self):
        print("Leaving 綜藝")

    
    # type drama 各國熱門戲劇
    def is_going_to_type_drama(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "各國熱門戲劇"
        else:
            return False

    def on_enter_type_drama(self, event):
        print("I'm entering 各國熱門戲劇\n")
        reply_token = event.reply_token
        send_text_drama_button(reply_token)
        # self.go_back()

    def on_exit_type_drama(self, *args, **kwargs):
        print("Leaving 各國熱門戲劇")

    # china
    def is_going_to_china(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "熱門陸劇"
        else:
            return False

    def on_enter_china(self, event):
        print("I'm entering china\n")
        reply_token = event.reply_token
        send_drama(reply_token, "china")
        send_back(reply_token)
        # self.go_back()

    def on_exit_china(self, *args, **kwargs):
        print("Leaving china")

    # hongkong
    def is_going_to_hongkong(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "熱門港劇"
        else:
            return False

    def on_enter_hongkong(self, event):
        print("I'm entering hongkong\n")
        reply_token = event.reply_token
        send_drama(reply_token, "hongkong")
        send_back(reply_token)
        # self.go_back()

    def on_exit_hongkong(self, *args, **kwargs):
        print("Leaving hongkong")

    # japan
    def is_going_to_japan(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "熱門日劇"
        else:
            return False

    def on_enter_japan(self, event):
        print("I'm entering japan\n")
        reply_token = event.reply_token
        send_drama(reply_token, "japan")
        send_back(reply_token)
        # self.go_back()

    def on_exit_japan(self, *args, **kwargs):
        print("Leaving japan")

    # korea
    def is_going_to_korea(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "熱門韓劇"
        else:
            return False

    def on_enter_korea(self, event):
        print("I'm entering korea\n")
        reply_token = event.reply_token
        send_drama(reply_token, "korea")
        send_back(reply_token)
        # self.go_back()

    def on_exit_korea(self, *args, **kwargs):
        print("Leaving korea")

    # america
    def is_going_to_america(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "熱門美劇"
        else:
            return False

    def on_enter_america(self, event):
        print("I'm entering week\n")
        reply_token = event.reply_token
        send_drama(reply_token, "america")
        send_back(reply_token)
        # self.go_back()

    def on_exit_america(self, *args, **kwargs):
        print("Leaving week")

    # england
    def is_going_to_england(self, event):
        if event.message.text:
            text = event.message.text
            return text.lower() == "熱門英劇"
        else:
            return False

    def on_enter_england(self, event):
        print("I'm entering week\n")
        reply_token = event.reply_token
        send_drama(reply_token, "england")
        send_back(reply_token)
        # self.go_back()

    def on_exit_england(self, *args, **kwargs):
        print("Leaving 熱門英劇")

    # --------------------------------------------------------
    # home/back
    # back
    def is_going_to_home(self, event):
        text = event.message.text
        return text.lower() == "回到首頁"

    def is_going_to_back(self, event):
        text = event.message.text
        return text.lower() == "回前一步"

    def on_enter_back(self, event):
        print("I'm entering back\n")
        reply_token = event.reply_token
        send_back(reply_token)
        self.go_back()

    def on_exit_back(self):
        print("Leaving back")