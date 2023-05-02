export default function Loading() {
  return (
    <div
      style={{
        height: "100%",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <style jsx>{`
        .loader {
          border: 10px solid #f3f3f3;
          border-top: 10px solid #1c2536;
          border-radius: 50%;
          width: 120px;
          height: 120px;
          animation: spin 2s linear infinite;
          margin: auto;
        }
        .loader-text {
          margin-bottom: -100px;
        }

        @keyframes spin {
          0% {
            transform: rotate(0deg);
          }
          100% {
            transform: rotate(360deg);
          }
        }
      `}</style>
      <div className="loader-text">Quantum computer generating optimal route</div>
      <div className="loader"></div>
    </div>
  );
}
