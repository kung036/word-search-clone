// 로그아웃
export const handleLogout = () => {
  window.localStorage.removeItem("token");
  window.location.reload();
};
