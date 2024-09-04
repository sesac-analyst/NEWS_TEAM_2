# NEWS_TEAM_2
---

### 참가자:
---
- 김도형, 이예림, 이종찬

### 프로젝트 설명
---
추천 시스템의 목표는 IT/과학에 관심이 있는 사용자들에게 맞춤형 뉴스 추천을 제공하는 것입니다.
IT/과학 분야에서는 최신 기술 동향을 파악하는 것이 중요하기 때문에 각 사용자의 관심사를 분석하여
관련 기사를 추천함으로써 기업 및 기술 동향을 잘 이해하고 반영할 수 있도록 돕습니다. 사용자가
흥미를 가질 가능성이 높은 뉴스를 제공하고 효율적으로 정보를 습득할 수 있도록 지원합니다.

### Sources
| Source | Link |
| --- | --- |
| Project Details | [News_Team2_Notion](https//www.notion.so/Team-2-d84dc41eead04a56a9835abe12851a02) |
| Data files | [News_Team2_Google_Drive](https://drive.google.com/drive/folders/1J_yoFFkmi9-Hk-OAeyv5tqjWsIToHyIG) |

### envs
---
Python version = 3.10


![Python Icon](https://img.icons8.com/color/48/python--v1.png) ![Numpy Icon](https://img.icons8.com/color/48/numpy.png) ![JupyterNotebook Icon](https://img.icons8.com/fluency/48/jupyter.png) ![VSCode Icon](https://img.icons8.com/dusk/64/visual-studio.png) ![pandas Icon](https://img.icons8.com/color/48/pandas.png) ![slack Icon](https://img.icons8.com/doodle/48/slack-new.png) ![google_drive Icon](https://img.icons8.com/color/48/google-drive--v2.png) ![notion Icon](https://img.icons8.com/color/48/notion--v1.png) 
	
## Github Convention
___
기본 브랜치: main

- COMMIT_TYPE
    - feat : 새로운 기능 추가
    - fix : 버그 수정
    - docs : 문서 추가 및 수정
    - style : 코드 포맷팅, 세미콜론 누락, 오타 수정 등
    - test : 테스트코드
    - refactor : 코드 리팩토링
    - chore : 빌드 업무 수정, 패키지 매니저 수정
- COMMIT_SUMMARY
    - 영어로 작성
    - 마침표를 붙이지 않음
    - 50자를 넘기지 않음

### Github Upload Procedure
---
1. create (if not already created) a branch with appropriate branch name (eg. feat/crawling/naver)
```bash
git checkout -b branch_name
```

- If the branch is already created, simply do

```bash
git checkout branch_name
```

2. add modified files that needs to be pushed
```bash
git add .
```

3. commit changes with appropriate commit message
```bash
git commit -m '[#(issue_ID)] COMMIT_TYPE: COMMIT_SUMMARY ([related MR_ID)'
```

4. push the commit to local branch
```bash
git push origin branch_name
```

5. Go to github repository and click on 'Compare & Pull Request'
6. compare and Merge. Delete the branch after merged
7. Delete the branch in local repository
```bash
git checkout main
git branch -D branch_name
```

### Github Ground Rules
---
1. Create Issue for the current task that you are working on
2. Notify teammates after pull requests
3. **Never** push anything or work on main branch
