export function copyToClipboard(url) {
  navigator.clipboard
    .writeText(url)
    .then(() => {
      // 성공적으로 복사되었음을 사용자에게 알려주는 작은 표시
      const toast = document.createElement("div");
      toast.textContent = "텍스트가 복사되었습니다.";
      toast.style.cssText = `
          position: fixed;
          bottom: 20px;
          left: 50%;
          transform: translateX(-50%);
          background-color: rgba(0, 0, 0, 0.7);
          color: #fff;
          padding: 10px 20px;
          border-radius: 5px;
          z-index: 9999;
        `;
      document.body.appendChild(toast);

      // 3초 후에 표시를 제거
      setTimeout(() => {
        toast.remove();
      }, 3000);
    })
    .catch((err) => {
      console.error("텍스트 복사 중 오류가 발생했습니다:", err);
    });
}
