<script>
  import sha256 from "js-sha256";
  import Header from "../components/Header.svelte";

  let form = {};

  // 비밀번호가 같은지 확인하는 함수
  function checkPassword() {
    const { password1, password2 } = form;
    return password1 === password2;
  }

  // 회원가입 정보를 서버로 보내는 함수
  const handleSubmit = async (event) => {
    if (!checkPassword()) {
      alert("비밀번호가 같지 않습니다.");
      return;
    }

    // 비밀번호 암호화
    const { password1 } = form;
    const sha256Password = sha256(password1);
    form = { ...form, password: sha256Password };

    // FormData 형태로 변경
    const formData = new FormData();
    for (const key in form) {
      formData.append(key, form[key]);
    }

    // 데이터 전송
    const serverUrl = import.meta.env.VITE_SERVER_URL;
    const res = await fetch(serverUrl + "/sign", {
      method: "POST",
      body: formData,
    });

    console.log(res.status);
    if (res.status === 200) {
      handleLogin();
    } else {
      alert("회원가입에 실패했습니다.");
    }
  };

  // 로그인 페이지로 이동하기
  const handleLogin = () => {
    window.localStorage.removeItem("token");
    window.location.hash = "/login";
    window.location.reload();
  };
</script>

<Header />

<div class="sign-box">
  <h1>회원가입</h1>
  <form id="signup-form" on:submit|preventDefault={handleSubmit}>
    <div class="sign-box__info">
      <div>
        <label for="id">아아디</label>
        <input type="text" id="id" bind:value={form.id} required />
      </div>
      <div>
        <label for="password1">패스워드</label>
        <input
          type="password"
          id="password1"
          bind:value={form.password1}
          required
        />
      </div>
      <div>
        <label for="password2">패스워드 확인</label>
        <input
          type="password"
          id="password2"
          bind:value={form.password2}
          required
        />
      </div>
      <div>
        <label for="name">이름</label>
        <input type="text" id="name" bind:value={form.name} required />
      </div>
    </div>
    <div class="sign-btn">
      <button type="submit">회원가입하기</button>
      <p>
        회원이 아니면
        <a href="/#/sign" on:click={handleLogin}> 로그인</a>
        을 해주세요
      </p>
    </div>
  </form>
</div>
