// 단어 그리드 생성
export function createWordGrid(n, words) {
  // 빈 그리드 생성
  let word_grid = createEmptyGrid(n);

  // 단어 랜덤 배치
  for (const word of words) {
    word_grid = placeWord(word, word_grid);
  }

  // 빈칸에 랜덤 알파벳 생성
  fillRandomLetters(word_grid);

  return word_grid;
}

// 빈 그리드 생성 함수
export function createEmptyGrid(n) {
  const grid = [];
  for (let i = 0; i < n; i++) {
    const row = Array(n).fill(" "); // N 길이의 공백으로 채워진 배열 생성
    grid.push(row);
  }
  return grid;
}

// 단어 랜덤배치
export function placeWord(word, grid) {
  const N = grid.length;
  const directions = [
    [0, 1], // 오른쪽
    [1, 0], // 아래쪽
    [1, 1], // 대각선(우하향)
    [-1, 1], // 대각선(우상향)
  ];

  const wordLength = word.length;
  let placed = false;
  let x;
  let y;
  let direction;

  // 단어 배치 여부 확인하기
  while (true) {
    let startX = Math.floor(Math.random() * N);
    let startY = Math.floor(Math.random() * N);
    direction = directions[Math.floor(Math.random() * directions.length)];

    x = startX;
    y = startY;

    for (let i = 0; i < wordLength; i++) {
      if (x >= 0 && x < N && y >= 0 && y < N && grid[x][y] === " ") {
        x += direction[0];
        y += direction[1];
        placed = true;
      } else {
        // 배치할 수 없는 경우
        placed = false;
        break;
      }
    }

    // if (placed) break;
    if (placed) {
      // 단어를 그리드에 배치하기
      x = startX;
      y = startY;
      for (let i = 0; i < wordLength; i++) {
        grid[x][y] = word[i];
        x += direction[0];
        y += direction[1];
      }
      break;
    }
  }

  return grid;
}

// 남은 빈 칸에 랜덤 알파벳 채우기
export function fillRandomLetters(grid) {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  for (let row = 0; row < grid.length; row++) {
    for (let col = 0; col < grid[row].length; col++) {
      if (grid[row][col] === " ") {
        const randomIndex = Math.floor(Math.random() * alphabet.length);
        grid[row][col] = alphabet[randomIndex];
      }
    }
  }
  return grid;
}
