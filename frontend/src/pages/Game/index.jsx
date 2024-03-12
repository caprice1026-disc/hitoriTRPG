const GamePage = () => {
  const [gameState, setGameState] = useState(null);

  useEffect(() => {
    // マウント時にゲームの状態をロードする
    const loadGameState = async () => {
      try {
        // ゲームの状態をデータベースから取得する
        const gameData = await fetchGameStateFromDB();
        setGameState(gameData);
      } catch (error) {
        console.error('ゲームの状態の取得に失敗しました:', error);
      }
    };

    loadGameState();
  }, []);

  return (
    <div>
      <Header />
      <main>
        {/* ゲーム画面のコンテンツをここに記述 */}
        {gameState ? (
          <div>
            <p>進行中のゲームがあります。</p>
            <button onClick={() => handleStartNewGame()}>初めから始める</button>
            <button onClick={() => handleResumeGame()}>続きから始める</button>
          </div>
        ) : (
          <div>
            <p>新しいゲームを開始します。</p>
            <WorldSetting />
            <CharacterSetting />
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
};