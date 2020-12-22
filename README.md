# 2020-2 Intelligent Robot
- 기부로봇 만들기 프로젝트



## 주요 기능
- 사람을 발견할 시 일정거리 (약 1m)이내로 겁근
    - 일회용 컵을 들고 있는 사람 우선 접근
- 일회용 컵을 판다 아래에 위치한 카메라에게 보여주면 플라스틱 vs 종이 판별하여 쓰레기 수거
- 화면 속 판다가 QR 코드로 전환되며 기부를 유도
- 송금 완료시 판다가 손을 흔들어 줌


## 시연영상

![KakaoTalk_Video_2020-12-22-11-26-51](https://user-images.githubusercontent.com/42709887/102842128-98b17480-4449-11eb-9dc9-61cfde20930f.gif)



## Requirements
- TX2 ROS Package
- python 3.7
- opencv 3.4.0.14


## 시나리오
![KakaoTalk_Photo_2020-12-22-11-25-26](https://user-images.githubusercontent.com/42709887/102841512-6ce1bf00-4448-11eb-8071-c166d6513fef.png)

## rpt_graph


## Screenshot
![KakaoTalk_Photo_2020-12-22-11-21-17](https://user-images.githubusercontent.com/42709887/102841245-ecbb5980-4447-11eb-868c-eb8223577473.jpeg)

![KakaoTalk_Photo_2020-12-22-11-18-54](https://user-images.githubusercontent.com/42709887/102841045-81718780-4447-11eb-8190-da33862b77b1.jpeg)

![KakaoTalk_Photo_2020-12-22-11-22-19](https://user-images.githubusercontent.com/42709887/102841317-0d83af00-4448-11eb-99e1-96d595b2016d.jpeg)



## Role
|Name|Main Role|
|------|---|
|정석훈|Team Leader, Human Detection|
|김동호|Robot Hardware 설계|
|문수림|ROS Software Architecture Design, UI (PyQt5)|
|정찬희|구동모터 제어, Infra(Real Sense Cam, Network)|
|안상현|UI Video 제작|
|정윤경|Latte Panda Gesture|

