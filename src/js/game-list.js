import { handleLogin } from "./login";

// 나의 게임 페이지로 이동하기
export const handleMyGame = () => {
  window.location.hash = "/myGame";
  window.location.reload();
};

// 게임 정보 받아오기
export const handleGame = async () => {
  // 서버 요청
  const serverUrl = import.meta.env.VITE_SERVER_URL;
  const accessToken = window.localStorage.getItem("token");
  const res = await fetch(serverUrl + "/games", {
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
