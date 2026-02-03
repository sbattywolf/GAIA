from scripts.sequence_manager import create_sequence
steps=[{'title':f'Investigate item {i}','detail':'Check logs and status'} for i in range(1,9)]
seq = create_sequence(None,'local',steps,'Test Large Sequence')
print('SEQ_ID=',seq)
