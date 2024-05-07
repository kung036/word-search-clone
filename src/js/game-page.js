const pageUrl = `http://localhost:5173/#/game/`;

// 게임 링크로 게임 페이지 이동
export function changeGamePage(url) {
  const game_id = url.split("#/game/")[1];
  window.localStorage.setItem("game_id", game_id);
  window.location.hash = "/game";
  window.location.reload();
}

// 게임 링크로 게임 페이지 이동
export function changeGamePageByGameId(game_id) {
  window.localStorage.setItem("game_id", game_id);
  window.location.hash = "/game";
  window.location.reload();
}
