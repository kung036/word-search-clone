<script>
  import { createWordGrid } from "../js/game";
  import { handleGameWords, handleGameInfo } from "../js/game-server";
  import { onMount } from "svelte";

  // 격자 생성
  let n = 7; // 초기 격자 크기

  // 게임 정보
  let title = "";
  let description = "";

  // 단어 정보
  let words = [];
  let word_grid = [];
  let gameStarted = false;

  // 타이머 정보
  let timer = 0;

  // 리액티브 변수로 타이머 표시 형식을 분:초로 변환
  let formattedTimer = formatTimer();

  // 게임 시작
  function startGame() {
    gameStarted = true;

    // 단어 그리드 출력
    word_grid = createWordGrid(n, words);

    // 타이머 시작
    startTimer();
  }

  // 타이머 시작
  function startTimer() {
    setInterval(() => {
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
  });
</script>

<div class="game-title">
  <h1>{title}</h1>
  <h3>description : {description}</h3>
</div>
<div class="timer">{formattedTimer}</div>

{#if gameStarted}
  <div class="game-aria">
    <div class="grid-container">
      {#each word_grid as row}
        <div class="grid-row">
          {#each row as cell}
            <div class="grid-cell">{cell}</div>
          {/each}
        </div>
      {/each}
    </div>

    <ol class="words">
      {#each words as word}
        <div>{word}</div>
      {/each}
    </ol>
  </div>
{:else}
  <button on:click={startGame}>게임 시작</button>
{/if}
