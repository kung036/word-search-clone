export function changeGamePage(url) {
  const game_id = url.split("#/game/")[1];
  window.localStorage.setItem("game_id", game_id);
  window.location.hash = "/game";
  window.location.reload();
}
