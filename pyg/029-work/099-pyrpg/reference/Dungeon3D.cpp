/* 省略(初期化) */
/* 省略(プレイヤーの移動処理) */
/* 省略(ミニマップに表示するプレイヤー位置（三角形を生成してる）) */
/* 省略（疑似3Dダンジョンを描画するための一つ一つの関数） */

// 描画関数（まとめ役）
void CDungeon3D::Draw(){
	MiniMap();
	DrawVisible();

	if (mGoal) DrawString(800, 480, "---- CLEAR!! ----\nPUSH F1 TO RERTY", COL_WHITE);

	DrawFormatString(480, 480, COL_WHITE, "PX PY %d %d\nmDirection %d",mt_player.x,mt_player.y, mDirection);
}

// ===============================================================================
// 疑似3Dダンジョン描画
void CDungeon3D::DrawVisible() {
	/*
	t_pos seach[VISIBLE*VISIBLE] = {
		{ 0, 0 },{ 1, 0 },{ 2, 0 },
		{ 0, 1 },{ 1, 1 },{ 2, 1 },
		{ 2, 0 },{ 2, 1 },{ 2, 2 } };
		*/

	SeachVisible();

	DrawBox(START_X_LEFT, START_Y_TOP, START_X_RIGHT, LONG_Y_UNDER, COL_GRAY_AISLE, true);
	DrawRectangle(START_X_LEFT, START_Y_UNDER, LONG_X_LEFT, LONG_Y_UNDER, START_X_RIGHT, START_Y_UNDER, LONG_X_RIGHT, LONG_Y_UNDER, COL_GRAY_AISLE, true);

	if (GetVisible(0, 0) == BLOCK)longLeft();
	if (GetVisible(1, 0) == BLOCK)longCenter();
	if (GetVisible(2, 0) == BLOCK)longRight();
	if (GetVisible(0, 1) == BLOCK)mediumLeft();
	if (GetVisible(1, 1) == BLOCK)mediumCenter();
	if (GetVisible(2, 1) == BLOCK)mediumRight();
	if (GetVisible(0, 2) == BLOCK)shortLeft();
	if (GetVisible(2, 2) == BLOCK)shortRight();

	VisibleMap();
}

// 視界描画
void CDungeon3D::VisibleMap() {
	for (int i = 0; i < VISIBLE; i++) {
		for (int j = 0; j < VISIBLE; j++) {
			switch (mapVisible[i][j]) {
			case NOUN: DrawBox(mt_mini.x + j * MINI_SIZE, mt_mini.y + 200 + i * MINI_SIZE,
				mt_mini.x + (j + 1) * MINI_SIZE, mt_mini.y + 200 + (i + 1) * MINI_SIZE, COL_GRAY, true); break;
			case BLOCK: DrawBox(mt_mini.x + j * MINI_SIZE, mt_mini.y + 200 + i * MINI_SIZE,
				mt_mini.x + (j + 1) * MINI_SIZE, mt_mini.y + 200 + (i + 1) * MINI_SIZE, COL_WHITE, true); break;
			case GOAL: DrawBox(mt_mini.x + j * MINI_SIZE, mt_mini.y + 200 + i * MINI_SIZE,
				mt_mini.x + (j + 1) * MINI_SIZE, mt_mini.y + 200 + (i + 1) * MINI_SIZE, COL_RED, true); break;
			default:
				break;
			}
		}
	}
}

// ミニマップ描画
void CDungeon3D::MiniMap() {
	for (int i = 0; i < MAP_SIZE; i++) {
		for (int j = 0; j < MAP_SIZE; j++) {
			switch (map[i][j]) {
			case NOUN: DrawBox(mt_mini.x + j * MINI_SIZE, mt_mini.y + i * MINI_SIZE,
				mt_mini.x + (j + 1) * MINI_SIZE, mt_mini.y + (i + 1) * MINI_SIZE, COL_GRAY, true); break;
			case BLOCK: DrawBox(mt_mini.x + j * MINI_SIZE, mt_mini.y + i * MINI_SIZE,
				mt_mini.x + (j + 1) * MINI_SIZE, mt_mini.y + (i + 1) * MINI_SIZE, COL_WHITE, true); break;
			case GOAL: DrawBox(mt_mini.x + j * MINI_SIZE, mt_mini.y + i * MINI_SIZE,
				mt_mini.x + (j + 1) * MINI_SIZE, mt_mini.y + (i + 1) * MINI_SIZE, COL_RED, true); break;
			case PLAYER: DrawBox(mt_mini.x + j * MINI_SIZE, mt_mini.y + i * MINI_SIZE,
				mt_mini.x + (j + 1) * MINI_SIZE, mt_mini.y + (i + 1) * MINI_SIZE, COL_BLUE_BACK, true);
				MiniPlayer(mt_mini.x + j * MINI_SIZE, mt_mini.y + i * MINI_SIZE); break;
			default:
				break;
			}
		}
	}
}

// 視界探索
void CDungeon3D::SeachVisible() {
	t_pos seachUP[VISIBLE*VISIBLE] = {
		{ -1,-2 },{  0,-2 },{ 1,-2 },
		{ -1,-1 },{  0,-1 },{ 1,-1 },
		{ -1, 0 },{  0, 0 },{ 1, 0 } };
	t_pos seachRIGHT[VISIBLE*VISIBLE] = {
		{  2,-1 },{  2, 0 },{ 2, 1 },
		{  1,-1 },{  1, 0 },{ 1, 1 },
		{  0,-1 },{  0, 0 },{ 0, 1 } };
	t_pos seachDOWN[VISIBLE*VISIBLE] = {
		{  1, 2 },{  0, 2 },{-1, 2 },
		{  1, 1 },{  0, 1 },{-1, 1 },
		{  1, 0 },{  0, 0 },{-1, 0 } };
	t_pos seachLEFT[VISIBLE*VISIBLE] = {
		{ -2, 1 },{ -2, 0 },{-2,-1 },
		{ -1, 1 },{ -1, 0 },{-1,-1 },
		{  0, 1 },{  0, 0 },{ 0,-1 } };

	int tx, ty;
	for (int i = 0; i < VISIBLE*VISIBLE; i++) {
		switch (mDirection) {
		case UP:
			tx = mt_player.x + seachUP[i].x;
			ty = mt_player.y + seachUP[i].y; break;
		case RIGHT:
			tx = mt_player.x + seachRIGHT[i].x;
			ty = mt_player.y + seachRIGHT[i].y; break;
		case DOWN:
			tx = mt_player.x + seachDOWN[i].x;
			ty = mt_player.y + seachDOWN[i].y; break;
		case LEFT:
			tx = mt_player.x + seachLEFT[i].x;
			ty = mt_player.y + seachLEFT[i].y; break;
		default:break;
		}

		if (ty < 0 || ty >= MAP_SIZE || tx < 0 || tx >= MAP_SIZE) {
			SetVisible(i % VISIBLE, i / VISIBLE, BLOCK);
		}
		else {
			SetVisible(i % VISIBLE, i / VISIBLE, GetMap(tx, ty));
		}
	}
}

