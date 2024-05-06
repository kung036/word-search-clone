export function changeGamePage(url) {
  const game_id = url.split("#/game/")[1];
  alert(game_id);
  window.localStorage.setItem("game_id", game_id);
  window.location.hash = "/game";
  window.location.reload();
}
