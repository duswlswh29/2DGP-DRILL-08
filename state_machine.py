from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE

class StateMachine: #상태를 관리하는
    def __init__(self,start_state,rules):
     self.cur_state=start_state #시작상태를 설정하고
     self.cur_state.enter(('START,0')) #더미로
     self.rules=rules#시작 상태로 진입
     pass

    def update(self):
        self.cur_state.do() #현재 상태의 동작 수행
        pass #현재는 하나의 상태가 들어있는 거고 이걸
    #커런트 스테이트가 아이들을 가리키고 있는 거다

    def draw(self):
        self.cur_state.draw() #현재 상태의 동작을그림
        pass

    def handle_state_event(self,state_event):
        for check_event in self.rules[self.cur_state].keys():
            if check_event(state_event):
                self.next_state=self.rules[self.cur_state][check_event]
                self.cur_state.exit(state_event)
                self.next_state.enter(state_event)
                print(f'{self.cur_state.__class__.__name__}==>{self.next_state.__class__.__name__}')
                self.cur_state=self.next_state
                return
                #printf(f'처리되지 않은 이벤트{event_to_string(event)}가 있습니다.')

        pass
