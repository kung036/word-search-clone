<script>
  let game_id = window.localStorage.getItem("game_id");

  // 서버로부터 데이터받아오기
  const handleSubmit = async (event) => {
    const serverUrl = import.meta.env.VITE_SERVER_URL;
    const accessToken = window.localStorage.getItem("token");
    const res = await fetch("/game", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    console.log(res.status);
    if (res.status == 401) {
      alert("로그인이 필요합니다!");
      handleLogin();
      return;
    }

    const data = await res.json();
  };

  // 로그인 페이지로 이동하기
  const handleLogin = () => {
    window.localStorage.removeItem("token");
    window.location.hash = "/login";
    window.location.reload();
  };
</script>

<div>
  {game_id}
</div>
