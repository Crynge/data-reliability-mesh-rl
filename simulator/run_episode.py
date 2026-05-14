from src.data_reliability_mesh import ReliabilityMeshEngine


def main() -> None:
    engine = ReliabilityMeshEngine()
    summary = engine.train(episodes=40)
    print(summary)


if __name__ == "__main__":
    main()

