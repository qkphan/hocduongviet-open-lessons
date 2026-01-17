# hocduongviet-open-lessons

Kho học liệu mở (Lessons + Exams) cho giáo dục phổ thông Việt Nam,
được thiết kế theo triết lý:
- Nội dung mở
- Kiểm soát chất lượng
- AI là công cụ, không phải nguồn chân lý

---

## 1. Kiến trúc tổng thể

Hệ thống gồm 4 lớp độc lập:

1. Content
   - lessons/
   - exams/

2. Schema & Rules
   - tools/schema/

3. Engine
   - tools/engine/

4. UI
   - ui/

Trung tâm dữ liệu: `school.db`

---

## 2. Quy ước exam

### Vòng đời đề thi

AI / GV → author/*.json  
→ validate  
→ normalize → exam.data.json  
→ import → school.db  
→ export → exam.export.json / PDF

### Quy ước tên file

| File | Ý nghĩa |
|----|----|
| exam.ai.json | AI tạo |
| exam.teacher.json | Giáo viên |
| exam.data.json | Chuẩn hệ thống |
| exam.export.json | Xuất bản |

---

## 3. Nguyên tắc

- Không sửa trực tiếp DB bằng tay
- Schema dùng chung nằm trong tools/schema
- Exams ≠ Lessons
- AI chỉ là một tác giả
