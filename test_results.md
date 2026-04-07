# Test Results - TravelBuddy Agent

- Generated at: `2026-04-07 15:51:23`
- Total cases: `5`

## Test 1 - Test 1 – Direct Answer (Không cần tool)

**Prompt:**

> Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

**Kỳ vọng:**

- Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian.  
- Không gọi tool nào.

**Tool calls:**

- Không có tool call

**Tool outputs:**

- Không có tool output

**Agent response:**

```text
Chào bạn! Thật vui khi được hỗ trợ bạn trong kế hoạch du lịch. Bạn có ý định đi đâu chưa? Hay bạn muốn mình gợi ý một số điểm đến thú vị ở Việt Nam? Nếu có ngân sách cụ thể và thời gian đi nữa thì càng tốt!
```

## Test 2 - Test 2 – Single Tool Call

**Prompt:**

> Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

**Kỳ vọng:**

- Gọi `search_flights("Hà Nội", "Đà Nẵng")`  
- Liệt kê 4 chuyến bay.

**Tool calls:**

- `search_flights` với args: `{'origin': 'Hà Nội', 'destination': 'Đà Nẵng'}`

**Tool outputs:**

- `search_flights`
```text
Danh sách chuyến bay Hà Nội -> Đà Nẵng:
1. Vietnam Airlines | 06:00 - 07:20 | economy | 1.450.000đ
2. Vietnam Airlines | 14:00 - 15:20 | business | 2.800.000đ
3. VietJet Air | 08:30 - 09:50 | economy | 890.000đ
4. Bamboo Airways | 11:00 - 12:20 | economy | 1.200.000đ
```

**Agent response:**

```text
Tôi đã tìm thấy một số chuyến bay từ Hà Nội đi Đà Nẵng cho bạn:

1. **Vietnam Airlines**
   - Giờ bay: 06:00 - 07:20
   - Hạng vé: Economy
   - Giá: 1.450.000đ

2. **Vietnam Airlines**
   - Giờ bay: 14:00 - 15:20
   - Hạng vé: Business
   - Giá: 2.800.000đ

3. **VietJet Air**
   - Giờ bay: 08:30 - 09:50
   - Hạng vé: Economy
   - Giá: 890.000đ

4. **Bamboo Airways**
   - Giờ bay: 11:00 - 12:20
   - Hạng vé: Economy
   - Giá: 1.200.000đ

Nếu bạn cần thêm thông tin hay muốn đặt vé, hãy cho tôi biết nhé!
```

## Test 3 - Test 3 – Multi-Step Tool Chaining

**Prompt:**

> Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

**Kỳ vọng:**

Agent phải tự chuỗi nhiều bước:

1. `search_flights("Hà Nội", "Phú Quốc")` → tìm vé rẻ nhất (1.100.000đ)  
2. `search_hotels("Phú Quốc", max_price phù hợp)` → gợi ý trong tầm giá  
3. `calculate_budget(5000000, "vé_bay:1100000,khách_sạn:...")` → tính còn lại  

→ Sau đó tổng hợp thành gợi ý hoàn chỉnh với bảng chi phí.

**Tool calls:**

- `search_flights` với args: `{'origin': 'Hà Nội', 'destination': 'Phú Quốc'}`
- `search_hotels` với args: `{'city': 'Phú Quốc', 'max_price_per_night': 2500000}`

**Tool outputs:**

- `search_flights`
```text
Danh sách chuyến bay Hà Nội -> Phú Quốc:
1. Vietnam Airlines | 07:00 - 09:15 | economy | 2.100.000đ
2. VietJet Air | 10:00 - 12:15 | economy | 1.350.000đ
3. VietJet Air | 16:00 - 18:15 | economy | 1.100.000đ
```
- `search_hotels`
```text
Danh sách khách sạn tại Phú Quốc:
1. 9Station Hostel | 2 sao | Dương Đông | Rating: 4.5 | 200.000đ/đêm
2. Sol by Meliá | 4 sao | Bãi Trường | Rating: 4.2 | 1.500.000đ/đêm
3. Lahana Resort | 3 sao | Dương Đông | Rating: 4.0 | 800.000đ/đêm
```

**Agent response:**

```text
Chuyến bay: 
1. Vietnam Airlines | 07:00 - 09:15 | economy | 2.100.000đ
2. VietJet Air | 10:00 - 12:15 | economy | 1.350.000đ
3. VietJet Air | 16:00 - 18:15 | economy | 1.100.000đ

Khách sạn:
1. 9Station Hostel | 2 sao | Dương Đông | Rating: 4.5 | 200.000đ/đêm
2. Sol by Meliá | 4 sao | Bãi Trường | Rating: 4.2 | 1.500.000đ/đêm
3. Lahana Resort | 3 sao | Dương Đông | Rating: 4.0 | 800.000đ/đêm

Tổng chi phí ước tính (giả sử bạn chọn chuyến bay VietJet Air lúc 10:00 và ở 9Station Hostel):
- Vé máy bay: 1.350.000đ
- Khách sạn (2 đêm): 200.000đ x 2 = 400.000đ

**Tổng chi phí:** 1.350.000đ + 400.000đ = 1.750.000đ

Gợi ý thêm: Bạn còn dư khoảng 3 triệu để thoải mái chi tiêu cho ăn uống và tham quan. Hãy thử những món hải sản tươi ngon tại Phú Quốc nhé! 🏖️✨
```

## Test 4 - Test 4 – Missing Info / Clarification

**Prompt:**

> Tôi muốn đặt khách sạn

**Kỳ vọng:**

- Agent hỏi lại:
  - Thành phố nào?
  - Bao nhiêu đêm?
  - Ngân sách bao nhiêu?
- Không gọi tool vội.

**Tool calls:**

- Không có tool call

**Tool outputs:**

- Không có tool output

**Agent response:**

```text
Bạn có thể cho mình biết bạn đang muốn đặt khách sạn ở thành phố nào và ngân sách tối đa mỗi đêm là bao nhiêu không?
```

## Test 5 - Test 5 – Guardrail / Refusal

**Prompt:**

> Giải giúp tôi bài tập lập trình Python về linked list

**Kỳ vọng:**

- Từ chối lịch sự  
- Nói rõ chỉ hỗ trợ về du lịch

**Tool calls:**

- Không có tool call

**Tool outputs:**

- Không có tool output

**Agent response:**

```text
Xin lỗi, nhưng mình không thể giúp bạn với bài tập lập trình. Tuy nhiên, nếu bạn cần tư vấn về các chuyến đi hay đặt phòng khách sạn, mình rất sẵn lòng giúp đỡ! Bạn dự định đi đâu hay có yêu cầu cụ thể nào về chuyến đi không?
```
