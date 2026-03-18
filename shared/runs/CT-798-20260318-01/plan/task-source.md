# CT-798: Socket integration for Recent Wins

## Ticket Info
- **Ticket:** CT-798
- **Status:** Ready for Testing
- **Priority:** Normal
- **Assignee:** Panda Sensei (Ihor)
- **Environment:** QA (https://minebit-casino.qa.sofon.one)

## Context
Recent Wins component now supports real-time updates via WebSocket.
- Previously: polling / static mock data
- Now: live win events stream (1 event per second)
- New config: `enableLiveUpdates` in Strapi (toggle WS/polling)

## Test Scope (First Test)

### Test Case 1: WebSocket Connection Validation
**Goal:** Verify WebSocket connection is established on the main page

**Preconditions:**
- QA environment: https://minebit-casino.qa.sofon.one
- Real player available for testing
- WebSocket endpoint available

**Steps:**
1. Open main page (https://minebit-casino.qa.sofon.one)
2. Open DevTools → Network tab → filter by "WS" (WebSocket)
3. Locate Recent Winners element on the page
4. Verify WebSocket connection exists
5. Check for WebSocket frames containing win events
6. Take screenshot of Network tab with WS connection
7. Take screenshot of Recent Winners element on the page

**Expected Result:**
- WebSocket connection established
- Network tab shows WS connection
- Recent Winners element displays with live updates

**Evidence Required:**
- Screenshot of Network tab showing WS connection
- Screenshot of Recent Winners element
- Console log (check for errors)

## Selector Reference
Recent Winners element example (from provided HTML):
```html
<div class="swiper-slide swiper-slide-active" data-swiper-slide-index="0">
  <div class="MuiGrid-root MuiGrid-container mui-style-vp3aja" data-cp="cmVjZW50V2lubmVyR3JpZENvbnRhaW5lclByb3Bz">
    <!-- Winner info grid -->
    <div class="MuiGrid-root MuiGrid-container MuiGrid-item mui-style-1p4d5x8" data-cp="d2lubmVySW5mb0dyaWRDb250YWluZXJQcm9wcw==">
      <p class="MuiTypography-root MuiTypography-body1 mui-style-n6ibh">TradeSmarter Options</p>
      <p class="MuiTypography-root MuiTypography-body1 mui-style-18hrtqo">te***@***.tech</p>
      <p class="MuiTypography-root MuiTypography-body1 mui-style-hfej9s">USD 31.86</p>
    </div>
  </div>
</div>
```

## Output Folder
`/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-798/`

## Notes
- No separate page for Recent Winners - it's an element on the main page
- Test with real player on QA environment
- WebSocket endpoint is available
