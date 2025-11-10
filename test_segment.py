from segmentation import segment_all

INPUT_PATH = r"D:\1.学习\4. UChicago\6.Research\Research Wang Group\Data Processing\Software Cut\20251101 CV full test (with oect)\4.7nF_Data.txt"
OUT_DIR    = r"D:\segments_out"
A_SECONDS  = 2.0

def main():
    res = segment_all(INPUT_PATH, OUT_DIR, A_SECONDS)
    print(f"peaks found: {len(res['peak_times'])}")
    print(f"segments saved: {len(res['saved_files'])}")
    if res["first_segment_df"] is not None:
        print("first segment preview:")
        print(res["first_segment_df"].head())

if __name__ == "__main__":
    main()
