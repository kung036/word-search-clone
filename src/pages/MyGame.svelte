<script>
  import { changeGamePageByGameId } from "../js/game-page";
  import { onMount } from "svelte";
  import Header from "../components/Header.svelte";
  import { handleGame } from "../js/game-list";

  let games;
  let print = false;

  async function clickBtn() {
    games = await handleGame();
    print = true;
  }

  onMount(async () => {
    await handleGame().then((data) => {
      games = data;
    });
    console.log(games);
  });
</script>

<Header />

<button on:click={clickBtn}>버튼</button>
{#if print}
  <div class="game-info-container">
    {#each games as game}
      <button
        on:click={() => changeGamePageByGameId(game.id)}
        class="game-info"
      >
        <div class="game-info-title">TITLE : {game.title}</div>
        <div class="game-info-description">
          DESCRIPTION : {game.description}
        </div>
      </button>
    {/each}
  </div>
{/if}

<!-- {#each games as game}
  <div>
    <p>ID: {game.id}</p>
    <p>Title: {game.title}</p>
    <p>Description: {game.description}</p>
    <p>User ID: {game.user_id}</p>
    <hr />
  </div>
{/each} -->
