# CPL-20172-Team5
종합 프로젝트 설계1

1. git bash를 연다 

2. 명령어 cd를 통해 내가 저장소로 사용할 폴더를 들어간다 폴더안에서 밑에꺼 진행해야함!
(user안에서 폴더 하나 만들어서 사용하는게 좋음)

3. git config --global user.email "깃허브 메일쓰면됨 따옴표까지"
git config --global user.name "깃이름쓰면됨"

---------처음 실행했을 때 초기화 끝

폴더안에 있는 상태에서 위에 초기화 끝내고
4. git remote add origin https://github.com/kswim/CPL-20172-Team5.git
(만약 origin 이 이미있다고 뜨면 add대신에 set-url 명령어 사용)
-> git remote -v 하면 원격저장소 주소확인가능

5. 만들어놓은 폴더에 파일들을 옮긴다(git bash 밖에서 하면됨)

6. git add * 하면 폴더안에 있는 모든 파일이 옮겨지고 git add (파일명) 하면 그 파일만 add됨

7. git status하면 add된 파일들 볼 수 있음

8. 넣을 파일이 잘 들어가있으면 git commit -m "메시지내용" 한다

9. git push origin master -f 해서 푸쉬!

10. git shortlog하면 어떤 commit들이 있는지 확인가능

11. 파일 올릴때 git diff 하면 어떤 소스코드에 어떤부분이 달라졌는지 확인 가능!!!!!
