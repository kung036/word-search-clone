<script>
  // 메인 페이지로 이동하기
  const handleMain = () => {
    window.location.hash = "/";
    window.location.reload();
  };
</script>

<button on:click={handleMain} class="home-btn">
  <img class="home-img" src="assets/home.svg" alt="" />
</button>
