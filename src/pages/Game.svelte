<script>
  import Header from "../components/Header.svelte";
  import { copyToClipboard } from "../js/click-share";
  import { isDiagonalOrStraight, toggleCellClass } from "../js/click-word";
  import { createWordGrid } from "../js/game";
  import { changeGamePage } from "../js/game-page";
  import {
    handleGameWords,
    handleGameInfo,
    handleScore,
    handleGetScore,
  } from "../js/game-server";
  import { onMount } from "svelte";

  const game_id = window.localStorage.getItem("game_id");
  const url = `http://localhost:5173/#/game/${game_id}`;

  // 격자 생성
  let n = 7; // 초기 격자 크기

  // 게임 정보
  let title = "";
  let description = "";

  // 단어 정보
  let words = [];
  let word_grid = [];
  let gameStarted = false;
  let gameFinish = false;

  // 타이머 정보
  let timer = 0;
  let timerId;

  // 리액티브 변수로 타이머 표시 형식을 분:초로 변환
  let formattedTimer = formatTimer();

  // 선택된 셀 배열
  let selectedCells = [];
  let selectedValues = [];

  // 찾은 단어수
  let countFindWords = 0;

  // score
  let scores;

  // 선택된 셀을 지우는 함수
  async function clearSelectedCells() {
    // 정답 여부 확인
    const selectAnswer = selectedValues.join("");
    if (words.includes(selectAnswer)) {
      // 정답 리스트에서 취소선하기
      const answerElements = document.querySelectorAll(`.words > div`);
      answerElements.forEach((element) => {
        if (element.textContent === selectAnswer) {
          element.classList.add("selected-answer");
        }
      });

      // 격자 색깔 변경
      const selectedCellElements = document.querySelectorAll(".selected-cell");
      selectedCellElements.forEach((cell) => {
        cell.classList.add("answer-cell");
      });

      countFindWords++;

      // 모든 단어를 찾은지 확인 → 게임 종료
      if (countFindWords === words.length) {
        // 타이머 종료
        clearInterval(timerId);

        // 게임 종료 안내
        gameFinish = true;

        // 스코어
        handleScore(formattedTimer);
        scores = await handleGetScore();
      }
    }

    // 선택한 셀 제거
    selectedCells = [];
    selectedValues = [];

    // 모든 선택된 셀의 클래스 제거
    const selectedCellElements = document.querySelectorAll(".selected-cell");
    selectedCellElements.forEach((cell) => {
      cell.classList.remove("selected-cell");
    });
  }

  // 게임 시작
  async function startGame() {
    gameStarted = true;

    // 단어 그리드 출력
    word_grid = createWordGrid(n, words);

    // 타이머 시작
    startTimer();
  }

  // 타이머 시작
  function startTimer() {
    timerId = setInterval(() => {
      timer++;
      formattedTimer = formatTimer();
    }, 1000);
  }

  // 타이머 표시 형식을 분:초로 변환하는 함수
  function formatTimer() {
    const minutes = Math.floor(timer / 60);
    const seconds = timer % 60;
    return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  }

  onMount(async () => {
    // 게임 정보
    const gameInfo = await handleGameInfo();
    title = gameInfo["title"];
    description = gameInfo["description"];

    // 단어 가져오기
    words = await handleGameWords();

    // 스코어 받아오기
    await handleGetScore().then((data) => {
      scores = data;
    });
  });

  // 격자 선택
  function handleCellClick(row, col) {
    // 대각선 또는 직선 방향인지 확인
    if (isDiagonalOrStraight(selectedCells.concat({ row, col }))) {
      // 셀 클래스 변경
      const isSelected = toggleCellClass(selectedCells, row, col);
      if (isSelected) {
        selectedValues.push(word_grid[row][col]);
      } else selectedValues.pop(); // 같은 격자 선택시
    }
  }
</script>

<Header />

<!-- 타이머 -->
<div>
  <h1 class="game-title">{title}</h1>
  <div class="game-description">
    <h3>description :</h3>
    <div class="game-description__info">
      {description}
    </div>
  </div>
  <div class="timer">{formattedTimer}</div>
</div>

{#if gameStarted}
  <!-- 격자 -->
  <div class="game-aria">
    <div class="grid-container">
      {#each word_grid as row, rowIndex}
        <div class="grid-row">
          {#each row as cell, colIndex}
            <div
              id={`cell-${rowIndex}-${colIndex}`}
              class="grid-item {selectedCells.find(
                (c) => c.row === rowIndex && c.col === colIndex
              )
                ? 'selected-cell'
                : ''}"
              role="button"
              tabindex="0"
              on:click={() => handleCellClick(rowIndex, colIndex)}
            >
              {cell}
            </div>
          {/each}
        </div>
      {/each}
    </div>

    <div>
      <!-- 단어 선택 버튼 -->
      <ol>
        <button on:click={clearSelectedCells}>단어 선택</button>
      </ol>
      <!-- 단어 출력 -->
      <ol class="words">
        {#each words as word}
          <div>{word}</div>
        {/each}
      </ol>

      <!-- 스코어 표시 -->
      <div class="score">
        <ol>
          <h2>스코어</h2>
          {#each scores as score, index}
            <div>
              {index + 1}위 {score.name}: {score.score}
            </div>
          {/each}
        </ol>
      </div>
    </div>
  </div>
{:else}
  <button on:click={startGame}>게임 시작</button>
{/if}

{#if gameFinish}
  <div class="container">
    <div class="centered">
      <!-- 게임 진행 메시지 및 스코어 표시 -->
      <h1>!! Game Finish !!</h1>
      <div class="score">
        <h2>스코어</h2>
        {#each scores as score, index}
          <div>
            {index + 1}위 {score.name}: {score.score}
          </div>
        {/each}
      </div>
      <button on:click={() => changeGamePage(url)} class="game-link__box">
        again!
      </button>
    </div>
  </div>
{/if}

<div class="game-link">
  <div class="game-link__text">게임 링크</div>
  <button on:click={() => changeGamePage(url)} class="game-link__box">
    {url}
  </button>
  <button on:click={() => copyToClipboard(url)} class="share-btn">
    <img class="share-img" src="assets/share.svg" alt="" />
  </button>
</div>
