# data_augmentation
You can extract frame from a video. You can use VGG image Annotator at https://www.robots.ox.ac.uk/~vgg/software/via/via_demo.html. You can use data augmentation by using labeling data and image. 

# Ball Detection
## 최종 목표 Task
- 드론에 장착된 카메라로 화면 상에 보이는 moving platform에 달려있는 공을 실시간으로 감지하여 안정적으로 접근하고 착륙

## 맡은 역할
1. 공이 포함된 이미지 데이터 수집
2. 클래스를 구별하지 않고 공 객체가 있는지 없는지 만을 판별해야 함.
3. 공 객체 bounding box를 직접 labeling 함.
4. 부족한 데이터 셋을 oversampling 하기 위하여 augmentation함. 
5. Augmentation한 이미지에 대하여 좌표를 알맞게 변환해주고 csv에 정해진 format으로 저장


# Drone Detection
## 최종 목표 Task
- 드론에 장착된 카메라로 화면 상에 나타난 드론을 실시간으로 감지하여 드론의 뒤를 따라다니게 함

## 맡은 역할
1. 드론이 포함된 이미지 데이터 수집
2. 클래스를 구별하지 않고 드론 객체가 있는지 없는지 만을 판별해야 함.
3. 드론 객체 bounding box를 직접 labeling 함.
4. 부족한 데이터 셋을 oversampling 하기 위하여 augmentation함. 
5. Augmentation한 이미지에 대하여 좌표를 알맞게 변환해주고 csv에 정해진 format으로 저장
