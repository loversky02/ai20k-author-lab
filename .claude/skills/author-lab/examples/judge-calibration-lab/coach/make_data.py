"""Regenerate data/answers.jsonl and data/pairs.jsonl. Deterministic; coach-only.

    python3 coach/make_data.py

The shop, its policies and every answer are invented for teaching. Human labels are the coach's
own rulings: correct facts and polite tone = pass; a wrong number, an invented policy, a refusal of
an answerable question, an off-topic or rude reply = fail. Eight items are deliberately hard for a
rule-based judge (marked hard=True) so every slice has real errors to analyse.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (question, reference, short_ok, long_ok, cited_ok, wrong_long)
Q = [
    ("Mình được đổi trả sách trong bao lâu?",
     "Được đổi trả trong 30 ngày kể từ ngày nhận hàng, sách còn nguyên tem.",
     "30 ngày kể từ khi nhận hàng bạn nhé.",
     "Bạn có thể đổi trả trong vòng 30 ngày kể từ ngày nhận hàng, miễn là sách còn nguyên tem và chưa bị viết vào.",
     "Theo mục Đổi trả, bạn được đổi trong 30 ngày kể từ ngày nhận, sách cần còn nguyên tem.",
     "Bạn có thể đổi trả trong vòng 90 ngày kể từ ngày nhận hàng, kể cả khi sách đã bóc tem, chỉ cần giữ hoá đơn."),
    ("Đơn bao nhiêu thì được miễn phí giao hàng?",
     "Đơn từ 300.000đ được miễn phí giao hàng; dưới mức đó phí là 25.000đ.",
     "Từ 300.000đ là miễn phí ship ạ.",
     "Đơn hàng từ 300.000đ trở lên được miễn phí giao hàng toàn quốc; đơn dưới mức này phí giao là 25.000đ.",
     "Theo mục Giao hàng: đơn từ 300.000đ miễn phí, dưới 300.000đ tính phí 25.000đ.",
     "Đơn hàng từ 500.000đ trở lên mới được miễn phí giao hàng, còn lại phí giao cố định là 40.000đ cho mọi khu vực."),
    ("Tổng đài hỗ trợ làm việc mấy giờ?",
     "Tổng đài làm việc từ 8:00 đến 21:00 mỗi ngày, kể cả cuối tuần.",
     "8:00 đến 21:00 hằng ngày ạ.",
     "Tổng đài hỗ trợ làm việc từ 8:00 đến 21:00 tất cả các ngày trong tuần, kể cả thứ Bảy và Chủ nhật.",
     "Theo mục Liên hệ, tổng đài mở 8:00–21:00 mỗi ngày, cả cuối tuần.",
     "Tổng đài làm việc từ 7:00 đến 23:00 từ thứ Hai đến thứ Sáu, cuối tuần nghỉ, bạn có thể để lại lời nhắn."),
    ("Giao hàng nội thành Hà Nội mất mấy ngày?",
     "Nội thành Hà Nội và TP.HCM giao trong 2 ngày; các tỉnh khác 4 ngày.",
     "Nội thành Hà Nội khoảng 2 ngày bạn nhé.",
     "Với địa chỉ nội thành Hà Nội, đơn hàng thường được giao trong 2 ngày làm việc; các tỉnh khác khoảng 4 ngày.",
     "Theo mục Giao hàng, nội thành Hà Nội nhận trong 2 ngày, tỉnh khác 4 ngày.",
     "Nội thành Hà Nội giao trong 5 ngày làm việc vì kho chính đặt ở TP.HCM, đơn gấp cần trả thêm phí hoả tốc."),
    ("Mua bao nhiêu tiền thì được 1 điểm thành viên?",
     "Cứ 10.000đ chi tiêu được tích 1 điểm thành viên.",
     "Mỗi 10.000đ được 1 điểm ạ.",
     "Chương trình thành viên tích 1 điểm cho mỗi 10.000đ bạn chi tiêu, điểm được cộng sau khi đơn giao thành công.",
     "Theo mục Thành viên: 10.000đ chi tiêu tương ứng 1 điểm.",
     "Chương trình thành viên tích 1 điểm cho mỗi 1.000đ chi tiêu và điểm được nhân đôi vào mọi ngày thứ Sáu trong tháng."),
    ("Gói quà có mất phí không?",
     "Dịch vụ gói quà có phí 15.000đ mỗi đơn.",
     "Có, 15.000đ một đơn ạ.",
     "Dịch vụ gói quà có tính phí 15.000đ cho mỗi đơn hàng, bạn chọn ở bước thanh toán và có thể kèm thiệp viết tay.",
     "Theo mục Dịch vụ thêm, gói quà tính 15.000đ mỗi đơn.",
     "Dịch vụ gói quà hoàn toàn miễn phí cho mọi đơn hàng, ngoài ra bạn còn được tặng thêm thiệp và hộp quà cao cấp."),
    ("Ebook đã tải về có được hoàn tiền không?",
     "Ebook đã tải về không được hoàn tiền; ebook chưa tải được hoàn trong 7 ngày.",
     "Đã tải thì không hoàn được bạn ạ.",
     "Ebook đã tải về thiết bị thì không được hoàn tiền; nếu bạn chưa tải, có thể yêu cầu hoàn tiền trong 7 ngày kể từ khi mua.",
     "Theo mục Ebook, sách đã tải không hoàn tiền, chưa tải thì hoàn trong 7 ngày.",
     "Ebook đã tải về vẫn được hoàn tiền 100% trong vòng 30 ngày nếu bạn thấy nội dung không như mong đợi, không cần lý do."),
    ("Đặt trước sách mới phải cọc bao nhiêu?",
     "Đặt trước cần cọc 20% giá sách, phần còn lại trả khi giao.",
     "Cọc 20% giá sách bạn nhé.",
     "Khi đặt trước sách mới phát hành, bạn cần đặt cọc 20% giá bìa; phần còn lại thanh toán khi nhận hàng.",
     "Theo mục Đặt trước: cọc 20% giá sách, trả nốt khi giao.",
     "Khi đặt trước sách mới bạn cần thanh toán đủ 100% giá bìa ngay lúc đặt, và khoản này không được hoàn nếu bạn huỷ."),
    ("Sinh viên có được giảm giá không?",
     "Sinh viên xuất trình thẻ được giảm 10%.",
     "Có, giảm 10% khi có thẻ sinh viên.",
     "Sinh viên được giảm 10% trên giá bìa khi xuất trình thẻ sinh viên còn hạn lúc nhận hàng hoặc tải ảnh thẻ khi đặt online.",
     "Theo mục Ưu đãi, sinh viên có thẻ được giảm 10%.",
     "Sinh viên được giảm 25% cho mọi đầu sách và miễn phí giao hàng không giới hạn, chỉ cần nhập mã trường khi thanh toán."),
    ("Thanh toán khi nhận hàng tối đa bao nhiêu?",
     "COD áp dụng cho đơn tối đa 2.000.000đ.",
     "Tối đa 2.000.000đ ạ.",
     "Hình thức thanh toán khi nhận hàng (COD) áp dụng cho đơn có giá trị tối đa 2.000.000đ; đơn lớn hơn cần chuyển khoản trước.",
     "Theo mục Thanh toán, COD áp dụng cho đơn đến 2.000.000đ.",
     "Thanh toán khi nhận hàng áp dụng cho mọi giá trị đơn hàng, không có giới hạn, kể cả đơn sỉ trên 10.000.000đ."),
    ("Sách bị lỗi in thì xử lý thế nào?",
     "Sách lỗi in được đổi mới miễn phí trong 30 ngày, cửa hàng chịu phí gửi.",
     "Đổi mới miễn phí trong 30 ngày bạn nhé.",
     "Nếu sách bị lỗi in, bạn được đổi cuốn mới miễn phí trong 30 ngày, cửa hàng chịu toàn bộ phí gửi hai chiều.",
     "Theo mục Đổi trả, sách lỗi in đổi mới miễn phí trong 30 ngày, shop chịu phí gửi.",
     "Sách lỗi in chỉ được giảm 10% cho lần mua sau, không đổi cuốn mới, và bạn tự chịu phí gửi trả về kho."),
    ("Có giao hàng ra nước ngoài không?",
     "Hiện chỉ giao trong Việt Nam, chưa giao quốc tế.",
     "Hiện chỉ giao trong nước bạn ạ.",
     "Hiện tại cửa hàng chỉ giao hàng trong lãnh thổ Việt Nam, chưa hỗ trợ giao quốc tế; bạn có thể nhờ người thân nhận hộ.",
     "Theo mục Giao hàng, hiện chỉ giao trong Việt Nam.",
     "Cửa hàng giao quốc tế đến 40 quốc gia với phí cố định 150.000đ, thời gian khoảng 7 ngày qua đối tác chuyển phát."),
    ("Điểm thành viên có hết hạn không?",
     "Điểm thành viên hết hạn sau 12 tháng kể từ ngày tích.",
     "Có, sau 12 tháng ạ.",
     "Điểm thành viên có hạn sử dụng 12 tháng kể từ ngày được tích; điểm sắp hết hạn sẽ được nhắc qua email trước 30 ngày.",
     "Theo mục Thành viên, điểm hết hạn sau 12 tháng kể từ ngày tích.",
     "Điểm thành viên không bao giờ hết hạn và có thể quy đổi thành tiền mặt bất cứ lúc nào với tỉ lệ 1 điểm bằng 1.000đ."),
    ("Mình có thể huỷ đơn sau khi đặt không?",
     "Được huỷ miễn phí khi đơn chưa chuyển sang trạng thái đang giao.",
     "Được, nếu đơn chưa giao đi ạ.",
     "Bạn có thể huỷ đơn miễn phí trong mục Đơn hàng của tôi khi đơn chưa chuyển sang trạng thái đang giao.",
     "Theo mục Đơn hàng, huỷ miễn phí khi đơn chưa ở trạng thái đang giao.",
     "Đơn đã đặt không thể huỷ dưới bất kỳ hình thức nào; nếu không nhận hàng bạn sẽ bị khoá tài khoản 6 tháng."),
    ("Có bán sách cũ không?",
     "Có khu sách cũ, mỗi cuốn được kiểm tra và ghi rõ tình trạng.",
     "Có mục sách cũ bạn nhé.",
     "Cửa hàng có khu sách cũ; mỗi cuốn đều được kiểm tra, chụp ảnh và ghi rõ tình trạng trước khi đăng bán.",
     "Theo mục Sách cũ, mỗi cuốn được kiểm tra và ghi tình trạng.",
     "Cửa hàng không bán sách cũ vì quy định bản quyền, mọi đầu sách đều là sách mới nhập trực tiếp từ nhà xuất bản."),
    ("Thẻ quà tặng dùng được bao lâu?",
     "Thẻ quà tặng có hạn 6 tháng kể từ ngày phát hành.",
     "6 tháng từ ngày phát hành ạ.",
     "Thẻ quà tặng có giá trị sử dụng trong 6 tháng kể từ ngày phát hành và dùng được nhiều lần đến khi hết số dư.",
     "Theo mục Thẻ quà tặng, hạn dùng 6 tháng kể từ ngày phát hành.",
     "Thẻ quà tặng có hạn 3 năm và có thể đổi lại thành tiền mặt tại quầy nếu bạn không muốn dùng nữa."),
    ("Mua sỉ có được chiết khấu không?",
     "Đơn từ 50 cuốn cùng đầu sách được chiết khấu 15%.",
     "Từ 50 cuốn được giảm 15% ạ.",
     "Với đơn mua sỉ từ 50 cuốn cùng một đầu sách, cửa hàng chiết khấu 15% và hỗ trợ xuất hoá đơn cho tổ chức.",
     "Theo mục Mua sỉ, đơn từ 50 cuốn cùng đầu sách được chiết khấu 15%.",
     "Mua sỉ từ 10 cuốn bất kỳ là được chiết khấu 40%, áp dụng cộng dồn với mã giảm giá và ưu đãi sinh viên."),
    ("Đổi địa chỉ giao hàng sau khi đặt được không?",
     "Được đổi địa chỉ khi đơn chưa đóng gói, qua tổng đài hoặc mục Đơn hàng.",
     "Được, nếu đơn chưa đóng gói ạ.",
     "Bạn đổi được địa chỉ giao hàng khi đơn chưa được đóng gói, bằng cách gọi tổng đài hoặc sửa trong mục Đơn hàng của tôi.",
     "Theo mục Đơn hàng, đổi địa chỉ được khi đơn chưa đóng gói.",
     "Địa chỉ giao hàng không thể thay đổi sau khi đặt; bạn phải huỷ đơn và đặt lại, phí huỷ là 20.000đ mỗi lần."),
    ("Có chương trình đọc thử không?",
     "Mỗi đầu sách có bản đọc thử 20 trang đầu trên trang sản phẩm.",
     "Có, đọc thử 20 trang đầu ạ.",
     "Mỗi đầu sách trên website có bản đọc thử 20 trang đầu ngay trên trang sản phẩm, không cần đăng nhập.",
     "Theo mục Đọc thử, mỗi sách có 20 trang đầu đọc thử trên trang sản phẩm.",
     "Bạn được đọc thử toàn bộ cuốn sách trong 48 giờ sau khi đăng ký thành viên trả phí 99.000đ mỗi tháng."),
    ("Có xuất hoá đơn VAT không?",
     "Có xuất hoá đơn VAT nếu yêu cầu trong 24 giờ sau khi đặt.",
     "Có, yêu cầu trong 24 giờ ạ.",
     "Cửa hàng xuất hoá đơn VAT cho cá nhân và doanh nghiệp nếu bạn gửi yêu cầu trong 24 giờ sau khi đặt hàng.",
     "Theo mục Hoá đơn, xuất VAT khi yêu cầu trong 24 giờ sau khi đặt.",
     "Cửa hàng chỉ xuất hoá đơn VAT cho đơn trên 5.000.000đ và phải yêu cầu trước khi đặt, sau đó không xuất bổ sung."),
]

REFUSAL = "Xin lỗi, hiện tại tôi không có thông tin về chính sách này, bạn vui lòng liên hệ bộ phận hỗ trợ để được tư vấn thêm."
OFFTOPIC = "Cảm ơn bạn đã quan tâm! Tháng này cửa hàng có rất nhiều đầu sách mới hấp dẫn, bạn hãy ghé mục Sách bán chạy để khám phá nhé."

# Hard cases: (question index, variant slot, answer, human label, why)
HARD = {
    (0, 0): ("Đọc chính sách trên web đi, 30 ngày, hỏi hoài.", "fail", "đúng số nhưng thô lỗ"),
    (3, 1): ("Nội thành Hà Nội 2 ngày, ngoài ra bạn được tặng kèm bookmark và túi vải miễn phí cho mọi đơn hàng.", "fail", "đúng số nhưng bịa thêm khuyến mãi"),
    (6, 2): ("Ebook bạn đã tải về rồi thì không hoàn được, nhưng ebook chưa tải vẫn hoàn trong vòng một tuần nhé.", "pass", "diễn đạt 7 ngày bằng chữ"),
    (9, 0): ("Tối đa 2.000.000đ, đơn lớn hơn bạn gọi 1900 6868 để được hỗ trợ chuyển khoản.", "pass", "thêm số tổng đài đúng, không có trong reference"),
    (12, 1): ("Điểm có hạn 12 tháng, và cửa hàng sẽ tự động gia hạn thêm 12 tháng cho thành viên hạng Vàng.", "fail", "đúng số nhưng bịa chính sách gia hạn"),
    (15, 2): ("Thẻ quà tặng dùng được nửa năm kể từ ngày phát hành, dùng nhiều lần đến khi hết tiền.", "pass", "diễn đạt 6 tháng thành nửa năm"),
    (17, 0): ("Ừ thì gọi tổng đài mà đổi, đơn chưa đóng gói thì được.", "fail", "đúng nội dung nhưng thô lỗ"),
    (19, 1): ("Có xuất VAT, bạn gửi yêu cầu trong 24 giờ, và mọi hoá đơn đều được giảm thêm 5% thuế cho khách thân thiết.", "fail", "bịa ưu đãi thuế"),
}

PATTERNS = [  # variant kinds per question, cycling
    ("short_ok", "long_ok", "wrong_long"),
    ("short_ok", "cited_ok", "refusal"),
    ("long_ok", "short_ok", "offtopic"),
]


def answer(qi, kind):
    q, ref, short_ok, long_ok, cited_ok, wrong_long = Q[qi]
    return {"short_ok": (short_ok, "pass"), "long_ok": (long_ok, "pass"), "cited_ok": (cited_ok, "pass"),
            "wrong_long": (wrong_long, "fail"), "refusal": (REFUSAL, "fail"), "offtopic": (OFFTOPIC, "fail")}[kind]


def main():
    rows, n = [], 0
    for qi, (q, ref, *_rest) in enumerate(Q):
        for slot, kind in enumerate(PATTERNS[qi % 3]):
            text, label = answer(qi, kind)
            hard = (qi, slot) in HARD
            if hard:
                text, label, _why = HARD[(qi, slot)]
            n += 1
            rows.append({"id": f"a{n:02d}", "slice": "ABC"[(qi + slot) % 3], "question": q, "reference": ref,
                         "answer": text, "human_label": label})
    pairs, m = [], 0
    for qi, (q, ref, short_ok, long_ok, cited_ok, wrong_long) in enumerate(Q):
        # good vs bad, in an order that alternates so position alone predicts nothing
        for good, bad in ((short_ok, wrong_long), (cited_ok, REFUSAL if qi % 2 else OFFTOPIC)):
            if m >= 30:
                break
            m += 1
            a, b, pref = (good, bad, "A") if m % 2 else (bad, good, "B")
            pairs.append({"id": f"p{m:02d}", "question": q, "reference": ref, "answer_a": a, "answer_b": b,
                          "human_pref": pref})
    (ROOT / "data").mkdir(exist_ok=True)
    with open(ROOT / "data" / "answers.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    with open(ROOT / "data" / "pairs.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(p, ensure_ascii=False) + "\n" for p in pairs)
    passes = sum(r["human_label"] == "pass" for r in rows)
    print(f"answers.jsonl: {len(rows)} rows, {passes} pass / {len(rows) - passes} fail; pairs.jsonl: {len(pairs)} rows")


if __name__ == "__main__":
    main()
