<script>
  import sha256 from "js-sha256";
  import Header from "../components/Header.svelte";

  let form = {};

  // 로그인하기
  const handleSubmit = async (event) => {
    // 비밀번호 암호화
    const { password } = form;
    const sha256Password = sha256(password);

    // FormData 형태로 변경
    const formData = new FormData();
    for (const key in form) {
      formData.append(key, form[key]);
    }
    formData.set("password", sha256Password);

    // 서버 요청
    const serverUrl = import.meta.env.VITE_SERVER_URL;
    const res = await fetch(serverUrl + "/login", {
      method: "POST",
      body: formData,
    });

    // 로그인 요청 성공 시
    const data = await res.json();
    const accessToken = data.access_token;
    if (res.status === 200) {
      alert("로그인에 성공했습니다.");
      handleMain(accessToken);
    } else if (res.status === 401) {
      // 로그인 실패 시
      alert("id 또는 password가 틀렸습니다.");
    }
  };

  // 회원가입 페이지로 이동하기
  const handleSign = () => {
    window.localStorage.setItem("token", "sign");
    window.location.hash = "/sign";
    window.location.reload();
  };

  // 메인 페이지로 이동하기
  const handleMain = (accessToken) => {
    window.localStorage.setItem("token", accessToken);
    window.location.hash = "/";
    window.location.reload();
  };
</script>

<Header />

<form id="login-form" on:submit|preventDefault={handleSubmit}>
  <div class="login-box">
    <h1>로그인</h1>
    <div class="login-box__info">
      <div>
        <label for="id"> 아아디</label>
        <input type="text" id="id" bind:value={form.id} required />
      </div>
      <div>
        <label for="password">패스워드</label>
        <input
          type="password"
          id="password"
          bind:value={form.password}
          required
        />
      </div>
    </div>
    <div>
      <button class="login-btn" type="submit">로그인</button>
    </div>
    <p>
      회원이 아니면
      <a href="/#/sign" on:click={handleSign}> 회원가입</a>
      을 해주세요
    </p>
  </div>
</form>
