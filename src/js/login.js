// 로그인 페이지로 이동하기
export const handleLogin = () => {
  window.localStorage.removeItem("token");
  window.location.hash = "/login";
  window.location.reload();
};
