import { createSlice, PayloadAction } from '@reduxjs/toolkit';

type State = {
  level?: string;
  cursor?: string;
};

const initialState: State = {};

const slice = createSlice({
  name: 'scenario',
  initialState,
  reducers: {
    setFilter(state, action: PayloadAction<Partial<State>>) {
      Object.assign(state, action.payload);
    },
    resetFilters() { return {}; }
  }
});

export const { setFilter, resetFilters } = slice.actions;
export default slice.reducer;

