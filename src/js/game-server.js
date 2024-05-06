import { handleLogin } from "./login";

// 게임 정보 받아오기
export const handleGameInfo = async (event) => {
  let game_id = window.localStorage.getItem("game_id");

  // 서버 요청
  const serverUrl = import.meta.env.VITE_SERVER_URL;
  const accessToken = window.localStorage.getItem("token");
  const res = await fetch(serverUrl + "/game/" + game_id, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  // 결과값 처리
  if (res.status == 401) {
    alert("로그인이 필요합니다!");
    handleLogin();
    return;
  }

  const data = await res.json();
  return data;
};

// 게임 단어 받아오기
export const handleGameWords = async (event) => {
  let game_id = window.localStorage.getItem("game_id");
  // 서버 요청
  const serverUrl = import.meta.env.VITE_SERVER_URL;
  const accessToken = window.localStorage.getItem("token");
  const res = await fetch(serverUrl + "/word/" + game_id, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  // 결과값 처리
  if (res.status == 401) {
    alert("로그인이 필요합니다!");
    handleLogin();
    return;
  }

  const data = await res.json();
  let words = await data["word"].split(",");

  return words;
};
