export const getTagStyle = (tagId: number, isSelected: boolean) => {
    if (tagId <= 50) { // Technical - Zoff Blue
        return isSelected
            ? 'bg-[#00A0E9]/15 border-[#00A0E9] text-[#00A0E9] font-bold'
            : 'bg-white border-[#00A0E9]/30 text-[#00A0E9] hover:bg-[#00A0E9]/5';
    } else if (tagId <= 100) { // Proposal - Zoff Orange
        return isSelected
            ? 'bg-[#F39800]/15 border-[#F39800] text-[#F39800] font-bold'
            : 'bg-white border-[#F39800]/30 text-[#F39800] hover:bg-[#F39800]/5';
    } else if (tagId <= 200) { // Scene - Zoff Green
        return isSelected
            ? 'bg-[#8FC31F]/15 border-[#8FC31F] text-[#8FC31F] font-bold'
            : 'bg-white border-[#8FC31F]/30 text-[#8FC31F] hover:bg-[#8FC31F]/5';
    } else { // Hobby - Zoff Purple
        return isSelected
            ? 'bg-[#951B81]/15 border-[#951B81] text-[#951B81] font-bold'
            : 'bg-white border-[#951B81]/30 text-[#951B81] hover:bg-[#951B81]/5';
    }
};

export const getTagBadgeStyle = (tagId: number) => {
    if (tagId <= 50) return 'bg-[#00A0E9]/10 border-[#00A0E9]/20 text-[#00A0E9]'; // Blue
    if (tagId <= 100) return 'bg-[#F39800]/10 border-[#F39800]/20 text-[#F39800]'; // Orange
    if (tagId <= 200) return 'bg-[#8FC31F]/10 border-[#8FC31F]/20 text-[#8FC31F]'; // Green
    return 'bg-[#951B81]/10 border-[#951B81]/20 text-[#951B81]'; // Purple
};

export const getTagTitleColor = (tagId: number) => {
    if (tagId <= 50) return 'text-[#00A0E9]';
    if (tagId <= 100) return 'text-[#F39800]';
    if (tagId <= 200) return 'text-[#8FC31F]';
    return 'text-[#951B81]';
}
