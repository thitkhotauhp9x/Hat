from hat.instructions.base_instruction import BaseInstruction


class TFQuestionCheck(BaseInstruction):
    tf_question: str

    def get_instruction(self) -> str:
        return """
Kiểm tra câu hỏi trắc nghiệm Đúng/ Sai sau có tuân thủ các nguyên tắc khi viết câu trắc nghiệm Đúng/Sai sau không.


Nguyên tắc khi viết câu trắc nghiệm Đúng/Sai

1. Mặc dù câu trắc nghiệm yêu cầu trả lời Đúng/Sai rất phù hợp để kiểm tra khả năng ghi nhớ,
 người viết câu hỏi vẫn nên chú ý nâng cao năng lực được trắc nghiệm, chẳng hạn khả năng giải thích,
 lý giải một hiện tượng, tránh kiểm tra việc ghi nhớ một cách máy móc thông tin đã được học, bằng
 cách không trích nguyên văn những câu viết, nhận định từ tài liệu mà diễn đạt lại các điều người
 học đã học dưới những hình thức mới.
 
2. Mỗi câu trắc nghiệm chỉ nên bao hàm một vấn đề cần kiểm tra, không nên đưa vào nhiều hơn một
 ý để tránh trường hợp câu hỏi nửa đúng, nửa sai.

3. Tránh sử dụng các từ ngữ có tính giới hạn đặc thù mang tính ám thị, có thể làm cho người đọc
 đoán mò câu hỏi, chỉ dựa trên ý nghĩa của các từ này. Một số từ mang ý nghĩ như trên như: nói chung,
 thông thường, thường thường, có thể, hầu hết, đa số. Những nhận định có sử dụng một trong những
 từ trên thường có đáp án và dễ dàng đoán mò là "Đúng". Ngược lại, những nhận định có sử dụng
 những từ mang ý nghĩa tuyệt đối như: mọi, các, tất cả, luôn luôn, nhất định,... thường có đáp án
 và được đoán mò là Sai.
 
 4. Câu trắc nghiệm yêu cầu Đúng/Sai cần phải được diễn đạt mạch lạc, rõ ràng để có thể xác định
được rõ là đúng hay sai, tránh các cách diễn đạt có thể gây hiểu nhầm, hoặc không thể xác định được
là đúng hay sai.

5. Không nên viết câu hỏi có chi tiết bẫy người học. Câu hỏi cần tập trung vào kiểm tra mức độ làm
chủ mục tiêu dạy học mà ta dự định đánh giá.

6. Hạn chế dùng câu phủ định, đặc biệt là câu có hai lần phủ định.

7. Mỗi nhận định để người học xác định là đúng hay sai cần là một lý trọn vẹn.

8. Để viết số lương, nên khai thác tối đa cách diễn đạt định lượng thay vì định tính để tăng tính
 chính xác của thông tin mà người học cần đánh giá là đúng hay sai, tránh gây tranh cãi đáp án.
 Một số từ định tính như: nhiều, ít, nhỏ, trẻ, già ....
"""
    pass
