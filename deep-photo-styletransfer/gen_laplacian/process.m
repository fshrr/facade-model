# list for the id of input images
id_list = [5]

pkg load image


for id_list_index = 1:numel(id_list)
    i = id_list(id_list_index)
    out_file = strcat('./processed/Input_Laplacian_3x3_1e-7_CSR', int2str(i), '.mat')
		data = load(['./generated/Input_Laplacian_3x3_1e-7_CSR' int2str(i) '.mat']);
		save "-mat7-binary" out_file data;
end
