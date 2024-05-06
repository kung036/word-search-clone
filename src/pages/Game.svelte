<script>
  import { createWordGrid, handleGameInfo } from "../js/game";
  import { handleGameWords } from "../js/game";
  import { onMount } from "svelte";

  // 격자 생성
  let n = 7; // 초기 격자 크기

  $: columnTemplate = `repeat(${n}, 50px)`;

  // 단어 출력
  // 페이지가 로드되면 게임 단어 받아오기
  let words = [];
  // let word_grid = createEmptyGrid(n);
  let word_grid = [];
  onMount(async () => {
    words = await handleGameWords();
    word_grid = createWordGrid(n, words);
    console.log(word_grid);

    // // 단어 랜덤 배치
    // for (const word of words) {
    //   word_grid = placeWord(word, word_grid);
    // }
  });
</script>

<h1>Play Word Game!!</h1>
<button on:click={handleGameInfo}>게임 가져오기</button>
<button on:click={handleGameWords}>단어 가져오기</button>

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
      <div>
        {word}
      </div>
    {/each}
  </ol>
</div>
