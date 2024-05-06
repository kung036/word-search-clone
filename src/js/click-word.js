// 격자 셀 클래스 변경 함수
export function toggleCellClass(selectedCells, row, col) {
  const cell = document.getElementById(`cell-${row}-${col}`);
  const index = selectedCells.findIndex(
    (cell) => cell.row === row && cell.col === col
  );

  if (index !== -1) {
    // 이미 선택된 셀을 다시 클릭한 경우 선택을 취소함
    cell.classList.remove("selected-cell");
    selectedCells.splice(index, 1); // 선택된 셀 정보 삭제
    return false; // 선택 취소됨을 나타내는 값 반환
  } else {
    // 새로운 셀을 클릭한 경우 선택을 추가함
    cell.classList.add("selected-cell");
    selectedCells.push({ row, col });
    return true; // 선택됨을 나타내는 값 반환
  }
}

// 대각선 또는 직선 방향인지 확인하는 함수
export function isDiagonalOrStraight(selectedCells) {
  // 선택된 셀들의 좌표 추출
  const rows = selectedCells.map((cell) => cell.row);
  const cols = selectedCells.map((cell) => cell.col);

  // 가로, 세로 방향인지 확인
  const isHorizontal = rows.every((row) => row === rows[0]);
  const isVertical = cols.every((col) => col === cols[0]);

  // 대각선 방향인지 확인
  const isDiagonal = rows.every((row, index) => {
    return Math.abs(row - rows[0]) === Math.abs(cols[index] - cols[0]);
  });

  // 연속된 값인지 확인
  if (isHorizontal || isVertical || isDiagonal) {
    for (let i = 1; i < selectedCells.length; i++) {
      const rowDiff = Math.abs(selectedCells[i].row - selectedCells[i - 1].row);
      const colDiff = Math.abs(selectedCells[i].col - selectedCells[i - 1].col);
      if (rowDiff > 1 || colDiff > 1) {
        return false;
      }
    }
    return true;
  }
  return false;
}
