from pathlib import Path
import json

DATA_FILE = Path("attendance.json")


def load_records():
    """저장 파일에서 출석 기록을 읽어 온다. 없으면 빈 목록."""
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_records(records):
    """출석 기록을 파일에 저장한다."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def add_attendance(records):
    """날짜와 이름을 입력받아 출석을 추가한다."""
    date = input("날짜 (예: 2026-11-03): ").strip()
    name = input("이름: ").strip()

    if not date or not name:
        print("날짜와 이름은 비울 수 없어요.")
        return

    # 같은 날, 같은 사람 중복 방지
    for r in records:
        if r["date"] == date and r["name"] == name:
            print("이미 등록된 출석이에요.")
            return

    records.append({"date": date, "name": name})
    save_records(records)
    print("저장했어요.")


def show_attendance(records):
    """전체 출석 목록을 보여 준다."""
    if not records:
        print("아직 기록이 없어요.")
        return
    print("\n[출석 목록]")
    for r in records:
        print(f'{r["date"]} - {r["name"]}')


def show_rate(records):
    """사람마다 출석률을 보여 준다."""
    if not records:
        print("아직 기록이 없어요.")
        return

    all_days = {r["date"] for r in records}   # 기록된 모든 날
    total = len(all_days)
    names = {r["name"] for r in records}       # 등장한 모든 사람

    print("\n[출석률]")
    for name in sorted(names):
        my_days = {r["date"] for r in records if r["name"] == name}
        rate = len(my_days) / total * 100
        print(f"{name}: {len(my_days)}/{total}일 ({rate:.1f}%)")


def main():
    records = load_records()
    while True:
        print("\n=== 스터디 출석부 ===")
        print("1. 출석 추가")
        print("2. 출석 목록")
        print("3. 출석률")
        print("0. 종료")

        choice = input("선택: ").strip()
        if choice == "1":
            add_attendance(records)
        elif choice == "2":
            show_attendance(records)
        elif choice == "3":
            show_rate(records)
        elif choice == "0":
            print("종료합니다.")
            break
        else:
            print("없는 메뉴예요.")


if __name__ == "__main__":
    main()
    