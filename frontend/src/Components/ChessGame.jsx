import { useState } from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";

export default function ChessGame() {

  const [game, setGame] = useState(new Chess());

  const [moves, setMoves] = useState([]);

  async function onDrop(sourceSquare, targetSquare) {

    const gameCopy = new Chess(game.fen());


    const move = gameCopy.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: "q",
    });

    if (move === null) {
      return false;
    }


    setMoves((prevMoves) => [
      ...prevMoves,
      `Player: ${move.san}`
    ]);

    setGame(new Chess(gameCopy.fen()));

    if (gameCopy.isGameOver()) {
      return true;
    }

    try {


      const response = await fetch(
        "http://localhost:3001/bestmove",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            fen: gameCopy.fen(),
          }),
        }
      );

      const data = await response.json();

      const bestMove = data.move;


      const engineMove = gameCopy.move({
        from: bestMove.slice(0, 2),
        to: bestMove.slice(2, 4),
        promotion: "q",
      });


      setMoves((prevMoves) => [
        ...prevMoves,
        `Engine: ${engineMove.san}`
      ]);


      setGame(new Chess(gameCopy.fen()));

    } catch (error) {

      console.error("Engine error:", error);

    }

    return true;
  }

  function startNewGame() {

    setGame(new Chess());

    setMoves([]);

  }

  return (
    <div
      style={{
        display: "flex",
        gap: "30px",
        padding: "20px",
      }}
    >

      <div>

        <Chessboard
          position={game.fen()}
          onPieceDrop={onDrop}
          boardWidth={600}
        />

        <button
          onClick={startNewGame}
          style={{
            marginTop: "20px",
            padding: "10px 20px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          New Game
        </button>

      </div>

      <div
        style={{
          width: "250px",
          border: "1px solid #ccc",
          padding: "15px",
          borderRadius: "8px",
          maxHeight: "650px",
          overflowY: "auto",
        }}
      >

        <h2>Moves</h2>

        {moves.length === 0 ? (
          <p>No moves yet</p>
        ) : (
          moves.map((move, index) => (
            <div
              key={index}
              style={{
                marginBottom: "8px",
              }}
            >
              {index + 1}. {move}
            </div>
          ))
        )}

      </div>

    </div>
  );
}